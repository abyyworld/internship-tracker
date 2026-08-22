#!/usr/bin/env python3
"""Keep the CV helper running, on whichever operating system this is.

The helper is a background service, not an application: it should start when
the machine does, restart if it stops, and never need a window kept open. Every
operating system agrees on that idea and disagrees on everything else, so the
platform-specific part is kept here and is deliberately small:

    macOS    a LaunchAgent plist in ~/Library/LaunchAgents, loaded with
             launchctl bootstrap
    Linux    a systemd user unit in ~/.config/systemd/user, enabled with
             systemctl --user; where systemd is absent, an XDG autostart entry
    Windows  a shortcut-free .cmd in the Startup folder, plus a Scheduled Task
             where schtasks is available

The Python that runs the bridge is identical everywhere, so what varies is only
how the machine is told to start it. Each installer writes its file, starts the
service, and returns what it did; verifying that the helper actually answers is
the caller's job, because "installed" and "working" are different claims.
"""

from __future__ import annotations

import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Any


LABEL = "com.autoapply.bridge"
UNIT = "autoapply-bridge"
PORT = 8765


def current_platform() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    return "linux"


def python_for(project: Path) -> Path:
    """The interpreter the service should run.

    A virtual environment inside the project is preferred, because that is
    where the dependencies were installed; whatever is running now is the
    fallback, which is right for a system-wide install.
    """
    candidates = [
        project / ".venv" / "bin" / "python",
        project / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return Path(sys.executable)


# ── macOS ────────────────────────────────────────────────────────────────────

def _xml(value: str) -> str:
    return (
        str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def macos_plist(project: Path, interpreter: Path) -> str:
    entries = "".join(
        f"\n\t\t<string>{_xml(part)}</string>"
        for part in (str(interpreter), "-m", "autoapply", "bridge")
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>Label</key>
\t<string>{LABEL}</string>
\t<key>ProgramArguments</key>
\t<array>{entries}
\t</array>
\t<key>WorkingDirectory</key>
\t<string>{_xml(str(project))}</string>
\t<key>RunAtLoad</key>
\t<true/>
\t<key>KeepAlive</key>
\t<true/>
\t<key>ProcessType</key>
\t<string>Background</string>
\t<key>StandardOutPath</key>
\t<string>{_xml(str(project / "private" / "bridge.log"))}</string>
\t<key>StandardErrorPath</key>
\t<string>{_xml(str(project / "private" / "bridge.log"))}</string>
</dict>
</plist>
"""


def install_macos(project: Path, interpreter: Path) -> dict[str, Any]:
    agents = Path.home() / "Library" / "LaunchAgents"
    agents.mkdir(parents=True, exist_ok=True)
    path = agents / f"{LABEL}.plist"
    path.write_text(macos_plist(project, interpreter), encoding="utf-8")
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", f"{domain}/{LABEL}"],
                   capture_output=True)
    started = subprocess.run(
        ["launchctl", "bootstrap", domain, str(path)], capture_output=True
    )
    if started.returncode != 0:
        subprocess.run(["launchctl", "load", "-w", str(path)], capture_output=True)
    return {"kind": "launchd", "file": str(path)}


# ── Linux ────────────────────────────────────────────────────────────────────

def systemd_unit(project: Path, interpreter: Path) -> str:
    # systemd splits ExecStart on whitespace, so an interpreter living under
    # "other projects/internship watcher" becomes three broken arguments unless
    # it is quoted.
    return f"""[Unit]
Description=Autoapply CV helper (local CV editor bridge)
After=network.target

[Service]
Type=simple
WorkingDirectory={project}
ExecStart="{interpreter}" -m autoapply bridge
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
"""


def autostart_desktop(project: Path, interpreter: Path) -> str:
    return f"""[Desktop Entry]
Type=Application
Name=Autoapply CV helper
Exec="{interpreter}" -m autoapply bridge
Path={project}
X-GNOME-Autostart-enabled=true
NoDisplay=true
"""


def install_linux(project: Path, interpreter: Path) -> dict[str, Any]:
    if shutil.which("systemctl"):
        units = Path.home() / ".config" / "systemd" / "user"
        units.mkdir(parents=True, exist_ok=True)
        path = units / f"{UNIT}.service"
        path.write_text(systemd_unit(project, interpreter), encoding="utf-8")
        subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
        started = subprocess.run(
            ["systemctl", "--user", "enable", "--now", f"{UNIT}.service"],
            capture_output=True,
        )
        # Without this the service stops at logout on most distributions.
        subprocess.run(["loginctl", "enable-linger", os.environ.get("USER", "")],
                       capture_output=True)
        if started.returncode == 0:
            return {"kind": "systemd", "file": str(path)}
        # systemctl exists but there is no user session behind it — a container,
        # or WSL without systemd. The unit is written for the day there is one,
        # and meanwhile the helper is started directly, because leaving someone
        # with a registered service that never runs is worse than either.
        _run_directly(project, interpreter)
        return {
            "kind": "systemd (unit written, started directly)",
            "file": str(path),
            "note": (
                "systemd could not start it here: "
                + (started.stderr or b"").decode(errors="replace").strip()[:200]
                + " — the helper is running now, and the unit will take over "
                "wherever a systemd user session exists."
            ),
        }
    autostart = Path.home() / ".config" / "autostart"
    autostart.mkdir(parents=True, exist_ok=True)
    path = autostart / f"{UNIT}.desktop"
    path.write_text(autostart_desktop(project, interpreter), encoding="utf-8")
    _run_directly(project, interpreter)
    return {"kind": "xdg-autostart", "file": str(path)}


def _run_directly(project: Path, interpreter: Path) -> None:
    """Start the helper now, detached from whatever started this."""
    log = project / "private" / "bridge.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    handle = open(log, "ab")
    subprocess.Popen(
        [str(interpreter), "-m", "autoapply", "bridge"],
        cwd=str(project),
        stdout=handle,
        stderr=handle,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )


# ── Windows ──────────────────────────────────────────────────────────────────

def windows_launcher(project: Path, interpreter: Path) -> str:
    # pythonw.exe runs it without a console window; python.exe is the fallback.
    windowless = interpreter.with_name("pythonw.exe")
    runner = windowless if windowless.exists() else interpreter
    return (
        "@echo off\r\n"
        f'cd /d "{project}"\r\n'
        f'start "" "{runner}" -m autoapply bridge\r\n'
    )


def install_windows(project: Path, interpreter: Path) -> dict[str, Any]:
    startup = (
        Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    )
    startup.mkdir(parents=True, exist_ok=True)
    path = startup / "autoapply-bridge.cmd"
    path.write_text(windows_launcher(project, interpreter), encoding="utf-8")
    # A scheduled task restarts it after a crash; the Startup entry alone only
    # covers logging in.
    if shutil.which("schtasks"):
        subprocess.run(
            ["schtasks", "/Create", "/F", "/SC", "ONLOGON", "/TN", UNIT,
             "/TR", f'"{path}"'],
            capture_output=True,
        )
    subprocess.Popen([str(path)], cwd=str(project), shell=True)
    return {"kind": "startup-folder", "file": str(path)}


# ── The one entry point ──────────────────────────────────────────────────────

INSTALLERS = {
    "macos": install_macos,
    "linux": install_linux,
    "windows": install_windows,
}


def install(project: Path | None = None) -> dict[str, Any]:
    """Install and start the helper for this machine's operating system."""
    project = Path(project or Path(__file__).resolve().parent.parent).resolve()
    interpreter = python_for(project)
    (project / "private").mkdir(parents=True, exist_ok=True)
    system = current_platform()
    result = INSTALLERS[system](project, interpreter)
    result.update({
        "platform": system,
        "project": str(project),
        "python": str(interpreter),
        "port": PORT,
    })
    return result


def uninstall(project: Path | None = None) -> dict[str, Any]:
    """Stop the helper and remove whatever made it start by itself."""
    system = current_platform()
    removed = []
    if system == "macos":
        path = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
        subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{LABEL}"],
                       capture_output=True)
        if path.exists():
            path.unlink()
            removed.append(str(path))
    elif system == "linux":
        subprocess.run(["systemctl", "--user", "disable", "--now", f"{UNIT}.service"],
                       capture_output=True)
        for path in (
            Path.home() / ".config" / "systemd" / "user" / f"{UNIT}.service",
            Path.home() / ".config" / "autostart" / f"{UNIT}.desktop",
        ):
            if path.exists():
                path.unlink()
                removed.append(str(path))
    else:
        path = (
            Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
            / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            / "autoapply-bridge.cmd"
        )
        if shutil.which("schtasks"):
            subprocess.run(["schtasks", "/Delete", "/F", "/TN", UNIT],
                           capture_output=True)
        if path.exists():
            path.unlink()
            removed.append(str(path))
    return {"platform": system, "removed": removed}
