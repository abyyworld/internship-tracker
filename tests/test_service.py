"""Installing the helper on whichever operating system this is.

The bridge itself is the same Python everywhere; what differs is how a machine
is told to start it. These check the files that carry that instruction, because
every one of them has a way of being silently wrong — a path with a space, a
console window nobody asked for, a service that dies at logout.
"""

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from autoapply import service


SPACED = Path("/Users/a/Desktop/other projects/internship watcher")
INTERPRETER = SPACED / ".venv" / "bin" / "python"


class PlatformDetectionTests(unittest.TestCase):
    def test_every_platform_has_an_installer(self):
        for system in ("macos", "linux", "windows"):
            self.assertIn(system, service.INSTALLERS)

    def test_unknown_systems_are_treated_as_linux(self):
        with patch("autoapply.service.platform.system", return_value="FreeBSD"):
            self.assertEqual(service.current_platform(), "linux")

    def test_a_project_virtualenv_is_preferred_over_the_running_python(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            venv = project / ".venv" / "bin"
            venv.mkdir(parents=True)
            (venv / "python").write_text("")
            self.assertEqual(service.python_for(project), venv / "python")

    def test_without_a_virtualenv_the_running_python_is_used(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(str(service.python_for(Path(directory))).endswith("python")
                            or "python" in str(service.python_for(Path(directory))))


class MacOSTests(unittest.TestCase):
    def test_the_plist_is_valid_and_survives_spaces(self):
        import plistlib

        spec = plistlib.loads(service.macos_plist(SPACED, INTERPRETER).encode())
        self.assertEqual(spec["Label"], service.LABEL)
        self.assertEqual(spec["ProgramArguments"],
                         [str(INTERPRETER), "-m", "autoapply", "bridge"])
        self.assertEqual(spec["WorkingDirectory"], str(SPACED))
        self.assertTrue(spec["RunAtLoad"])
        self.assertTrue(spec["KeepAlive"])

    def test_xml_special_characters_in_a_folder_name_are_escaped(self):
        import plistlib

        awkward = Path("/Users/a/R&D <work>")
        spec = plistlib.loads(
            service.macos_plist(awkward, awkward / "python").encode()
        )
        self.assertEqual(spec["WorkingDirectory"], str(awkward))


class LinuxTests(unittest.TestCase):
    def test_the_unit_quotes_an_interpreter_path_containing_spaces(self):
        # systemd splits ExecStart on whitespace, so an unquoted path under
        # "other projects" becomes three arguments and the service never starts.
        unit = service.systemd_unit(SPACED, INTERPRETER)
        self.assertIn(f'ExecStart="{INTERPRETER}" -m autoapply bridge', unit)
        self.assertIn(f"WorkingDirectory={SPACED}", unit)

    def test_the_unit_restarts_the_helper_and_starts_at_login(self):
        unit = service.systemd_unit(SPACED, INTERPRETER)
        self.assertIn("Restart=always", unit)
        self.assertIn("WantedBy=default.target", unit)

    def test_the_autostart_fallback_is_a_valid_desktop_entry(self):
        entry = service.autostart_desktop(SPACED, INTERPRETER)
        self.assertTrue(entry.startswith("[Desktop Entry]"))
        self.assertIn("Type=Application", entry)
        self.assertIn(f'Exec="{INTERPRETER}" -m autoapply bridge', entry)

    def test_systemd_is_used_when_available_and_lingering_is_enabled(self):
        with tempfile.TemporaryDirectory() as home:
            with patch("pathlib.Path.home", lambda: Path(home)), \
                 patch("autoapply.service.shutil.which", return_value="/bin/systemctl"), \
                 patch("autoapply.service.subprocess.run") as run, \
                 patch.dict(os.environ, {"USER": "tester"}):
                result = service.install_linux(SPACED, INTERPRETER)
            self.assertEqual(result["kind"], "systemd")
            self.assertTrue(Path(result["file"]).exists())
            called = [call.args[0] for call in run.call_args_list]
            self.assertIn(["systemctl", "--user", "daemon-reload"], called)
            # Without lingering the service stops at logout on most distributions.
            self.assertTrue(any(c[:2] == ["loginctl", "enable-linger"] for c in called))

    def test_without_systemd_it_falls_back_to_an_autostart_entry(self):
        with tempfile.TemporaryDirectory() as home:
            with patch("pathlib.Path.home", lambda: Path(home)), \
                 patch("autoapply.service.shutil.which", return_value=None), \
                 patch("autoapply.service.subprocess.Popen") as popen:
                result = service.install_linux(SPACED, INTERPRETER)
            self.assertEqual(result["kind"], "xdg-autostart")
            self.assertTrue(Path(result["file"]).exists())
            # And it starts the helper now rather than only at the next login.
            self.assertTrue(popen.called)


class WindowsTests(unittest.TestCase):
    def test_the_launcher_prefers_pythonw_so_no_console_window_appears(self):
        with tempfile.TemporaryDirectory() as directory:
            scripts = Path(directory) / "Scripts"
            scripts.mkdir()
            (scripts / "pythonw.exe").write_text("")
            launcher = service.windows_launcher(Path(directory), scripts / "python.exe")
            self.assertIn("pythonw.exe", launcher)

    def test_it_falls_back_to_python_when_pythonw_is_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            interpreter = Path(directory) / "python.exe"
            launcher = service.windows_launcher(Path(directory), interpreter)
            self.assertIn(str(interpreter), launcher)

    def test_the_launcher_changes_drive_and_directory(self):
        launcher = service.windows_launcher(Path("D:/work/x y"), Path("D:/work/x y/python.exe"))
        self.assertIn("cd /d", launcher)
        self.assertIn("-m autoapply bridge", launcher)
        # Batch files need CRLF endings.
        self.assertIn("\r\n", launcher)


class LauncherTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def test_a_launcher_exists_for_every_platform(self):
        for name in ("start-autoapply.command", "start-autoapply.sh",
                     "start-autoapply.bat"):
            self.assertTrue((self.ROOT / name).is_file(), name)

    def test_the_unix_launchers_are_executable(self):
        for name in ("start-autoapply.command", "start-autoapply.sh"):
            mode = (self.ROOT / name).stat().st_mode
            self.assertTrue(mode & 0o111, f"{name} is not executable")

    def test_every_launcher_installs_the_service_rather_than_holding_a_window(self):
        linux = (self.ROOT / "start-autoapply.sh").read_text()
        windows = (self.ROOT / "start-autoapply.bat").read_text()
        for text in (linux, windows):
            self.assertIn("install-service", text)


if __name__ == "__main__":
    unittest.main()
