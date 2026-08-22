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
    """Start the helper now, detached from whatever started this.

    The log is a convenience, not a condition: a project folder that cannot be
    written to is a reason to lose the log, never a reason to leave the person
    with no helper running.
    """
    log = project / "private" / "bridge.log"
    try:
        log.parent.mkdir(parents=True, exist_ok=True)
        handle: Any = open(log, "ab")
    except OSError:
        handle = subprocess.DEVNULL
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


def install(project: Path | None = None, *, update: bool = True) -> dict[str, Any]:
    """Install and start the helper for this machine's operating system.

    The checkout is brought up to date first. A service pointed at stale code
    is the failure this whole file exists to end: it comes back at every login,
    it never asks for attention, and it goes on running the bug someone already
    fixed. Installing without updating would just re-register that.
    """
    project = Path(project or Path(__file__).resolve().parent.parent).resolve()
    freshened = freshen_checkout(project) if update else {"skipped": True}
    interpreter = python_for(project)
    (project / "private").mkdir(parents=True, exist_ok=True)
    system = current_platform()
    result = INSTALLERS[system](project, interpreter)
    result.update({
        "platform": system,
        "project": str(project),
        "python": str(interpreter),
        "port": PORT,
        "update": freshened,
        "commit": checkout_commit(project),
    })
    return result


def describe_install(result: dict[str, Any]) -> list[str]:
    """What install() did, in lines fit for a window someone is watching.

    Kept here rather than in each launcher: three shell scripts describing the
    same JSON three ways is how they end up disagreeing about what happened.
    """
    update = result.get("update") or {}
    lines = []
    if update.get("updated"):
        lines.append(f"Updated  : {update.get('was')} → {update.get('commit')}")
    elif update.get("reason"):
        lines.append(f"Not updated: {update['reason']}")
    elif not update.get("skipped"):
        lines.append(f"Code     : already current ({result.get('commit') or '?'})")
    if update.get("moved_to"):
        lines.append(f"Followed : GitHub's {update['moved_to']} — "
                     "this checkout had drifted and could not fast-forward")
    if update.get("backup_branch"):
        lines.append(f"Kept     : what was here is on the branch {update['backup_branch']}")
    if update.get("stashed"):
        lines.append("Parked   : your own edits are stashed — "
                     "restore them with  git stash pop")
    lines.append(f"Installed: {result.get('file') or result.get('kind') or 'the service'}")
    if result.get("note"):
        lines.append(f"Note     : {result['note']}")
    return lines


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


# ── Which code is installed, and updating it ─────────────────────────────────
# A helper installed once and left alone is the point of this file, and it is
# also the reason a fix can take weeks to reach the machine having the problem.
# So the running helper can pull its own updates: the person using it never has
# to open a terminal to receive one.

def checkout_commit(project: Path | None = None) -> str:
    """The commit this copy of the code is checked out at, or "".

    Read out of .git rather than by running git, because /health is polled and
    spawning a process per poll to answer "which code is this" is a bad trade.
    """
    project = Path(project or Path(__file__).resolve().parent.parent)
    git = project / ".git"
    try:
        if git.is_file():  # a worktree or submodule: .git points elsewhere
            pointer = git.read_text(encoding="utf-8")
            git = Path(pointer.split("gitdir:", 1)[1].strip())
        head = (git / "HEAD").read_text(encoding="utf-8").strip()
        if head.startswith("ref:"):
            ref = head.split(":", 1)[1].strip()
            loose = git / ref
            if loose.exists():
                head = loose.read_text(encoding="utf-8").strip()
            else:  # the ref has been packed away
                head = ""
                packed = git / "packed-refs"
                for line in packed.read_text(encoding="utf-8").splitlines():
                    if line.endswith(f" {ref}"):
                        head = line.split(" ", 1)[0]
                        break
    except (OSError, IndexError, ValueError):
        return ""
    return head[:7] if len(head) >= 7 else ""


def _git(project: Path, *args: str, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(project), *args],
        capture_output=True, text=True, timeout=timeout,
    )


AUTO_UPDATE_INTERVAL = 6 * 60 * 60   # how often the helper looks for a fix
AUTO_UPDATE_FIRST_CHECK = 90         # after starting, before the first look
IDLE_BEFORE_RESTART = 300            # nothing may be in flight when it swaps


def auto_update_enabled(home: Path | None = None) -> bool:
    """Whether the helper may pull its own updates.

    On by default: a background service nobody ever opens is exactly the thing
    that quietly runs code from months ago. Off with AUTOAPPLY_NO_UPDATE=1, or
    by creating a file called no-auto-update in the private folder — no terminal
    needed for either.
    """
    if os.environ.get("AUTOAPPLY_NO_UPDATE", "").strip():
        return False
    return not (home and (Path(home) / "no-auto-update").exists())


def update_checkout(
    project: Path | None = None, *, park_local_edits: bool = True,
) -> dict[str, Any]:
    """Fast-forward the checkout the helper is running from.

    Deliberately narrow. It never switches branch — that would move someone's
    work out from under them without asking — and it never discards anything:
    asked for by hand, local edits are parked with git stash and the answer
    says so, so the way back is always `git stash pop`.

    An unattended caller passes park_local_edits=False and nothing is parked,
    because nobody is there to read where their work went. It is not refused
    either: git will not overwrite a modified file to fast-forward — it stops
    and names the file — so the working tree is safe without help, and edits
    to files the update does not touch survive the pull. Refusing on any dirt
    at all would freeze updates for good on a checkout where anything local
    has rewritten a generated file.
    """
    project = Path(project or Path(__file__).resolve().parent.parent).resolve()
    if not (project / ".git").exists():
        return {"updated": False,
                "reason": "This copy of the code is not a git checkout, "
                          "so there is nothing to pull."}
    if not shutil.which("git"):
        return {"updated": False,
                "reason": "git is not installed, so the code cannot update itself."}
    try:
        head = _git(project, "rev-parse", "--short", "HEAD", timeout=30)
        if head.returncode != 0:
            return {"updated": False,
                    "reason": (head.stderr or "git could not read this checkout").strip()}
        was = head.stdout.strip()
        branch = _git(project, "rev-parse", "--abbrev-ref", "HEAD", timeout=30).stdout.strip()

        stashed = False
        dirty = bool(_git(project, "status", "--porcelain", timeout=60).stdout.strip())
        if dirty and park_local_edits:
            stashed = _git(
                project, "stash", "push", "-u", "-m", "autoapply self-update",
            ).returncode == 0

        state = {"was": was, "commit": was, "branch": branch,
                 "stashed": stashed, "dirty": dirty and not stashed}
        fetched = _git(project, "fetch", "origin", "--quiet")
        if fetched.returncode != 0:
            detail = fetched.stderr.strip().splitlines()
            return {**state, "updated": False,
                    "reason": "Could not reach GitHub: "
                              + (detail[-1] if detail else "the fetch failed")}
        pulled = _git(project, "pull", "--ff-only", "--quiet")
        now = _git(project, "rev-parse", "--short", "HEAD", timeout=30).stdout.strip() or was
    except (OSError, subprocess.SubprocessError) as exc:
        return {"updated": False, "reason": f"git could not be run: {exc}"}

    result = {**state, "commit": now, "updated": now != was}
    if now == was and pulled.returncode != 0:
        detail = pulled.stderr.strip().splitlines()
        # The usual cause is a branch that has diverged, which a fast-forward
        # cannot fix and this function must not paper over.
        result["reason"] = (detail[-1] if detail else
                            "The branch could not be fast-forwarded.")
    return result


def remote_default_branch(project: Path) -> str:
    """The branch GitHub serves as default, as this clone understands it."""
    head = _git(project, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD", timeout=30)
    if head.returncode == 0 and head.stdout.strip():
        return head.stdout.strip().rsplit("/", 1)[-1]
    for guess in ("main", "master"):
        if _git(project, "rev-parse", "--verify", "--quiet",
                f"origin/{guess}", timeout=30).returncode == 0:
            return guess
    return ""


def freshen_checkout(project: Path | None = None) -> dict[str, Any]:
    """Bring the checkout up to date for someone who is standing right here.

    update_checkout is the careful one: fast-forward or nothing, because it
    runs unattended. This is the installer's version and it has a harder job.
    Someone has gone and double-clicked a file precisely because they are
    running old code, so leaving them on old code — because the branch had
    drifted, or HEAD was detached, or the branch was never pushed — fails at
    the only thing they asked for.

    So it fast-forwards where it can, and where it cannot it moves the checkout
    onto what GitHub actually serves. Nothing is lost doing that: everything
    uncommitted is stashed first, and any commit that would be left behind is
    kept on a backup branch this names in the answer.
    """
    project = Path(project or Path(__file__).resolve().parent.parent).resolve()
    if not (project / ".git").exists():
        return {"updated": False, "reason": (
            "This folder is not a git checkout, so it cannot receive updates. "
            "Clone the repository and run this from the clone.")}
    if not shutil.which("git"):
        return {"updated": False,
                "reason": "git is not installed, so the code cannot be updated."}
    try:
        head = _git(project, "rev-parse", "--short", "HEAD", timeout=30)
        if head.returncode != 0:
            return {"updated": False,
                    "reason": (head.stderr or "git could not read this checkout").strip()}
        was = head.stdout.strip()
        branch = _git(project, "rev-parse", "--abbrev-ref", "HEAD", timeout=30).stdout.strip()

        stashed = False
        if _git(project, "status", "--porcelain", timeout=60).stdout.strip():
            stashed = _git(
                project, "stash", "push", "-u", "-m", "autoapply install",
            ).returncode == 0

        fetched = _git(project, "fetch", "origin", "--quiet")
        if fetched.returncode != 0:
            detail = fetched.stderr.strip().splitlines()
            return {"updated": False, "was": was, "commit": was, "branch": branch,
                    "stashed": stashed,
                    "reason": "Could not reach GitHub: "
                              + (detail[-1] if detail else "the fetch failed")}

        detached = branch == "HEAD"
        pulled = None
        if not detached:
            pulled = _git(project, "pull", "--ff-only", "--quiet")
        now = _git(project, "rev-parse", "--short", "HEAD", timeout=30).stdout.strip() or was

        moved = ""
        backup = ""
        if detached or (pulled is not None and pulled.returncode != 0):
            # The branch will not fast-forward, so follow the remote instead.
            # Anything about to be left off a branch is given one first.
            default = remote_default_branch(project)
            if default:
                backup = f"autoapply-before-{was}"
                _git(project, "branch", backup, was, timeout=30)
                switched = _git(project, "checkout", "-B", default,
                                f"origin/{default}", timeout=60)
                if switched.returncode == 0:
                    moved = default
                    branch = default
                    now = (_git(project, "rev-parse", "--short", "HEAD", timeout=30)
                           .stdout.strip() or now)
                else:
                    _git(project, "branch", "-D", backup, timeout=30)
                    backup = ""
    except (OSError, subprocess.SubprocessError) as exc:
        return {"updated": False, "reason": f"git could not be run: {exc}"}

    result = {"was": was, "commit": now, "branch": branch,
              "stashed": stashed, "updated": now != was}
    if moved:
        result["moved_to"] = moved
        result["backup_branch"] = backup
    elif pulled is not None and pulled.returncode != 0 and now == was:
        detail = pulled.stderr.strip().splitlines()
        result["reason"] = (detail[-1] if detail else
                            "The branch could not be fast-forwarded.")
    return result


def running_under_service() -> bool:
    """Whether this machine's service manager is the one keeping the helper up.

    If it is, restarting is its job and the new code takes over by itself. If
    it is not, something started the helper by hand and stopping this process
    would leave nothing running.
    """
    system = current_platform()
    try:
        if system == "macos":
            return subprocess.run(
                ["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"],
                capture_output=True, timeout=15,
            ).returncode == 0
        if system == "linux":
            done = subprocess.run(
                ["systemctl", "--user", "is-active", f"{UNIT}.service"],
                capture_output=True, text=True, timeout=15,
            )
            return done.stdout.strip() == "active"
        if not shutil.which("schtasks"):
            return False
        return subprocess.run(
            ["schtasks", "/Query", "/TN", UNIT], capture_output=True, timeout=15,
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _self_command() -> list[str]:
    """The command that would start this process again.

    `python -m autoapply bridge` leaves argv[0] as the path to __main__.py, and
    running that file directly breaks its relative imports — so the -m form is
    reconstructed rather than replayed.
    """
    argv = list(sys.argv)
    if argv and Path(argv[0]).name == "__main__.py":
        return [sys.executable, "-m", Path(argv[0]).resolve().parent.name, *argv[1:]]
    return [sys.executable, *argv]


def restart() -> dict[str, Any]:
    """Replace the running helper with one started from the code on disk.

    Where a service manager owns the helper, it is asked to do the replacing,
    because it will keep the new process alive the same way it kept this one.
    Where nothing owns it, this process re-executes itself: the listening
    socket closes on exec and the new process binds it a moment later.
    """
    system = current_platform()
    try:
        if system == "macos":
            done = subprocess.run(
                ["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/{LABEL}"],
                capture_output=True, text=True, timeout=30,
            )
        elif system == "linux":
            done = subprocess.run(
                ["systemctl", "--user", "restart", f"{UNIT}.service"],
                capture_output=True, text=True, timeout=30,
            )
        elif shutil.which("schtasks"):
            subprocess.run(["schtasks", "/End", "/TN", UNIT],
                           capture_output=True, timeout=30)
            done = subprocess.run(["schtasks", "/Run", "/TN", UNIT],
                                  capture_output=True, text=True, timeout=30)
        else:
            done = subprocess.CompletedProcess([], 1, "", "no service manager")
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "detail": str(exc)}

    if done.returncode == 0:
        return {"ok": True, "detail": "the service manager is restarting the helper"}

    command = _self_command()
    try:
        os.execv(command[0], command)
    except OSError as exc:  # pragma: no cover - exec replaces the process
        return {"ok": False,
                "detail": (done.stderr or "").strip() or str(exc)}
    return {"ok": True, "detail": "restarted in place"}  # pragma: no cover
