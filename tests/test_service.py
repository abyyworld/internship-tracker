"""Installing the helper on whichever operating system this is.

The bridge itself is the same Python everywhere; what differs is how a machine
is told to start it. These check the files that carry that instruction, because
every one of them has a way of being silently wrong — a path with a space, a
console window nobody asked for, a service that dies at logout.
"""

import contextlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from autoapply import service


# A path with a space in it, because that is what breaks these files: systemd
# splits ExecStart on whitespace and a plist is XML. Used only where nothing is
# written — anything that installs for real gets a temporary folder of its own,
# since a test that writes outside its sandbox fails on every machine that is
# not the one it was written on.
SPACED = Path("/Users/a/Desktop/other projects/internship watcher")
INTERPRETER = SPACED / ".venv" / "bin" / "python"


@contextlib.contextmanager
def spaced_project():
    """A real project folder whose path contains a space."""
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "other projects" / "internship watcher"
        binaries = project / ".venv" / "bin"
        binaries.mkdir(parents=True)
        interpreter = binaries / "python"
        interpreter.write_text("", encoding="utf-8")
        yield project, interpreter


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
        from unittest.mock import Mock

        with tempfile.TemporaryDirectory() as home:
            with patch("pathlib.Path.home", lambda: Path(home)), \
                 patch("autoapply.service.shutil.which", return_value="/bin/systemctl"), \
                 patch("autoapply.service.subprocess.run",
                       return_value=Mock(returncode=0, stderr=b"")) as run, \
                 patch.dict(os.environ, {"USER": "tester"}):
                result = service.install_linux(SPACED, INTERPRETER)
            self.assertEqual(result["kind"], "systemd")
            self.assertTrue(Path(result["file"]).exists())
            called = [call.args[0] for call in run.call_args_list]
            self.assertIn(["systemctl", "--user", "daemon-reload"], called)
            # Without lingering the service stops at logout on most distributions.
            self.assertTrue(any(c[:2] == ["loginctl", "enable-linger"] for c in called))

    def test_systemd_without_a_user_session_still_leaves_a_running_helper(self):
        """A container, or WSL without systemd: systemctl exists and cannot
        start anything. Registering a service that never runs and calling it
        installed is the worst of the available outcomes."""
        from unittest.mock import Mock

        with tempfile.TemporaryDirectory() as home, spaced_project() as (project, python):
            with patch("pathlib.Path.home", lambda: Path(home)), \
                 patch("autoapply.service.shutil.which", return_value="/bin/systemctl"), \
                 patch("autoapply.service.subprocess.run",
                       return_value=Mock(returncode=1, stderr=b"Failed to connect to bus")), \
                 patch("autoapply.service.subprocess.Popen") as popen:
                result = service.install_linux(project, python)
            self.assertTrue(Path(result["file"]).exists())
            self.assertIn("started directly", result["kind"])
            self.assertIn("Failed to connect to bus", result["note"])
            self.assertTrue(popen.called, "the helper was not started at all")

    def test_without_systemd_it_falls_back_to_an_autostart_entry(self):
        with tempfile.TemporaryDirectory() as home, spaced_project() as (project, python):
            with patch("pathlib.Path.home", lambda: Path(home)), \
                 patch("autoapply.service.shutil.which", return_value=None), \
                 patch("autoapply.service.subprocess.Popen") as popen:
                result = service.install_linux(project, python)
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


class CheckoutCommitTests(unittest.TestCase):
    """Which code is on disk, answered without running git.

    /health is polled — by the opener page, by the editor, by the installer —
    so this is read out of .git directly, and that parsing has to survive the
    two shapes a ref can take.
    """

    def test_it_matches_what_git_says(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = _repo(Path(directory) / "repo")
            expected = _git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
            self.assertEqual(service.checkout_commit(repo), expected)

    def test_a_packed_ref_is_still_found(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = _repo(Path(directory) / "repo")
            expected = _git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
            _git(repo, "pack-refs", "--all")
            self.assertEqual(service.checkout_commit(repo), expected)

    def test_somewhere_that_is_not_a_checkout_says_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(service.checkout_commit(Path(directory)), "")


class UpdateCheckoutTests(unittest.TestCase):
    """Pulling the fix into the copy that is actually running.

    The failure this exists to prevent is a helper installed once and left for
    weeks, answering with code the repository no longer has. The failures it
    must not cause are worse: losing someone's local edits, or moving them onto
    a branch they did not choose.
    """

    def test_it_fast_forwards_to_the_new_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _commit(origin, "later.txt", "the fix")

            report = service.update_checkout(clone)

            self.assertTrue(report["updated"], report)
            self.assertNotEqual(report["was"], report["commit"])
            self.assertEqual((clone / "later.txt").read_text(), "the fix")

    def test_an_unchanged_checkout_says_so_without_claiming_an_update(self):
        with tempfile.TemporaryDirectory() as directory:
            _origin, clone = _origin_and_clone(Path(directory))

            report = service.update_checkout(clone)

            self.assertFalse(report["updated"])
            self.assertEqual(report["was"], report["commit"])
            self.assertNotIn("reason", report)

    def test_local_edits_are_parked_and_recoverable_never_discarded(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            (clone / "seed.txt").write_text("something I was in the middle of")
            _commit(origin, "later.txt", "the fix")

            report = service.update_checkout(clone)

            self.assertTrue(report["updated"])
            self.assertTrue(report["stashed"])
            _git(clone, "stash", "pop")
            self.assertEqual((clone / "seed.txt").read_text(),
                             "something I was in the middle of")

    def test_an_unattended_update_keeps_unrelated_local_edits_and_still_pulls(self):
        """Refusing on any dirt at all freezes updates for good.

        A checkout where anything local has rewritten a generated file would
        never update again. git protects the working tree by itself during a
        fast-forward, so edits to files the update does not touch survive it.
        """
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            (clone / "seed.txt").write_text("edited here")
            _commit(origin, "later.txt", "the fix")

            report = service.update_checkout(clone, park_local_edits=False)

            self.assertTrue(report["updated"], report)
            self.assertFalse(report["stashed"])
            self.assertEqual((clone / "seed.txt").read_text(), "edited here")
            self.assertEqual((clone / "later.txt").read_text(), "the fix")

    def test_an_unattended_update_will_not_overwrite_a_modified_file(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _commit(origin, "seed.txt", "changed upstream")
            (clone / "seed.txt").write_text("changed here")

            report = service.update_checkout(clone, park_local_edits=False)

            self.assertFalse(report["updated"])
            self.assertTrue(report["reason"])
            # The edit is still there, which is the only part that matters.
            self.assertEqual((clone / "seed.txt").read_text(), "changed here")

    def test_it_stays_on_the_branch_it_found(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _git(clone, "checkout", "-b", "mine")
            _commit(origin, "later.txt", "the fix")

            report = service.update_checkout(clone)

            self.assertEqual(report["branch"], "mine")
            self.assertEqual(_git(clone, "rev-parse", "--abbrev-ref", "HEAD")
                             .stdout.strip(), "mine")

    def test_a_diverged_branch_reports_the_reason_rather_than_success(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _commit(origin, "theirs.txt", "upstream")
            _commit(clone, "mine.txt", "local")

            report = service.update_checkout(clone)

            self.assertFalse(report["updated"])
            self.assertIn("reason", report)
            self.assertTrue(report["reason"])

    def test_being_unable_to_reach_the_remote_is_said_plainly(self):
        with tempfile.TemporaryDirectory() as directory:
            _origin, clone = _origin_and_clone(Path(directory))
            _git(clone, "remote", "set-url", "origin",
                 str(Path(directory) / "gone.git"))

            report = service.update_checkout(clone)

            self.assertFalse(report["updated"])
            self.assertIn("Could not reach GitHub", report["reason"])

    def test_a_folder_that_is_not_a_checkout_cannot_update_itself(self):
        with tempfile.TemporaryDirectory() as directory:
            report = service.update_checkout(Path(directory))

            self.assertFalse(report["updated"])
            self.assertIn("not a git checkout", report["reason"])


class FreshenCheckoutTests(unittest.TestCase):
    """Installing is what someone does *because* they are on old code.

    update_checkout runs unattended and may only fast-forward. This one runs
    because a person went and double-clicked a file, and leaving them on old
    code — because the branch drifted, or HEAD was detached — fails at the one
    thing they asked for. It may follow the remote, so what these check is that
    it never loses anything doing so.
    """

    def test_it_fast_forwards_like_the_unattended_one(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _commit(origin, "later.txt", "the fix")

            report = service.freshen_checkout(clone)

            self.assertTrue(report["updated"], report)
            self.assertEqual((clone / "later.txt").read_text(), "the fix")
            self.assertNotIn("moved_to", report)

    def test_a_diverged_branch_follows_the_remote_and_keeps_what_was_here(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _commit(origin, "theirs.txt", "upstream")
            _commit(clone, "mine.txt", "work of my own")
            mine = _git(clone, "rev-parse", "--short", "HEAD").stdout.strip()

            report = service.freshen_checkout(clone)

            self.assertTrue(report["updated"], report)
            self.assertEqual(report["moved_to"], "main")
            self.assertEqual((clone / "theirs.txt").read_text(), "upstream")
            # Nothing was thrown away: the commit that was here is on a branch.
            backup = report["backup_branch"]
            self.assertEqual(
                _git(clone, "rev-parse", "--short", backup).stdout.strip(), mine)
            self.assertEqual(
                _git(clone, "show", f"{backup}:mine.txt").stdout, "work of my own")

    def test_a_detached_head_is_put_back_on_the_remote_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            _commit(origin, "later.txt", "the fix")
            _git(clone, "checkout", "--detach", "HEAD")

            report = service.freshen_checkout(clone)

            self.assertEqual(report["moved_to"], "main")
            self.assertEqual(
                _git(clone, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), "main")
            self.assertEqual((clone / "later.txt").read_text(), "the fix")

    def test_local_edits_are_parked_before_any_of_that_and_are_recoverable(self):
        with tempfile.TemporaryDirectory() as directory:
            origin, clone = _origin_and_clone(Path(directory))
            (clone / "seed.txt").write_text("half-finished")
            _commit(origin, "seed.txt", "changed upstream")

            report = service.freshen_checkout(clone)

            self.assertTrue(report["stashed"])
            self.assertTrue(report["updated"])
            # The update took the upstream version of the same file, and the
            # half-finished one is sitting in the stash — which is what being
            # told "git stash pop" has to mean.
            self.assertEqual((clone / "seed.txt").read_text(), "changed upstream")
            self.assertTrue(_git(clone, "stash", "list").stdout.strip())
            self.assertIn("half-finished",
                          _git(clone, "stash", "show", "-p", "stash@{0}").stdout)

    def test_a_folder_that_is_not_a_checkout_says_so_instead_of_pretending(self):
        with tempfile.TemporaryDirectory() as directory:
            report = service.freshen_checkout(Path(directory))

            self.assertFalse(report["updated"])
            self.assertIn("not a git checkout", report["reason"])

    def test_installing_updates_first_unless_told_not_to(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            with patch("autoapply.service.freshen_checkout",
                       return_value={"updated": True, "was": "a", "commit": "b"}) as fresh, \
                 patch.dict(service.INSTALLERS,
                            {"linux": lambda *a: {"kind": "systemd", "file": "unit"}}), \
                 patch("autoapply.service.current_platform", return_value="linux"):
                installed = service.install(project)
                self.assertTrue(fresh.called)
                self.assertTrue(installed["update"]["updated"])

                fresh.reset_mock()
                installed = service.install(project, update=False)
                self.assertFalse(fresh.called)
                self.assertTrue(installed["update"]["skipped"])

    def test_what_it_did_is_said_in_lines_a_person_can_read(self):
        said = "\n".join(service.describe_install({
            "file": "/home/a/.config/systemd/user/autoapply-bridge.service",
            "update": {"updated": True, "was": "aaa1111", "commit": "bbb2222",
                       "moved_to": "main", "backup_branch": "autoapply-before-aaa1111",
                       "stashed": True},
        }))
        self.assertIn("aaa1111 → bbb2222", said)
        self.assertIn("main", said)
        self.assertIn("autoapply-before-aaa1111", said)
        self.assertIn("git stash pop", said)
        self.assertIn("autoapply-bridge.service", said)

        current = "\n".join(service.describe_install(
            {"file": "unit", "commit": "ccc3333", "update": {"updated": False}}))
        self.assertIn("already current (ccc3333)", current)

        blocked = "\n".join(service.describe_install(
            {"file": "unit", "update": {"updated": False,
                                        "reason": "Could not reach GitHub"}}))
        self.assertIn("Could not reach GitHub", blocked)


class RestartTests(unittest.TestCase):
    def test_macos_asks_launchd_to_replace_the_process(self):
        completed = subprocess.CompletedProcess([], 0, "", "")
        with patch("autoapply.service.current_platform", return_value="macos"), \
             patch("autoapply.service.subprocess.run", return_value=completed) as run:
            self.assertTrue(service.restart()["ok"])
        self.assertIn("kickstart", run.call_args[0][0])

    def test_linux_asks_systemd(self):
        completed = subprocess.CompletedProcess([], 0, "", "")
        with patch("autoapply.service.current_platform", return_value="linux"), \
             patch("autoapply.service.subprocess.run", return_value=completed) as run:
            self.assertTrue(service.restart()["ok"])
        self.assertEqual(run.call_args[0][0][:3], ["systemctl", "--user", "restart"])

    def test_with_no_service_manager_the_process_re_executes_itself(self):
        failed = subprocess.CompletedProcess([], 1, "", "no such service")
        with patch("autoapply.service.current_platform", return_value="linux"), \
             patch("autoapply.service.subprocess.run", return_value=failed), \
             patch("autoapply.service.os.execv") as execv:
            service.restart()
        self.assertTrue(execv.called)

    def test_the_module_form_is_reconstructed_not_replayed(self):
        # python -m autoapply leaves argv[0] pointing at __main__.py, and
        # running that file directly breaks its relative imports.
        with patch("autoapply.service.sys.argv",
                   [str(Path(service.__file__).parent / "__main__.py"), "bridge"]):
            command = service._self_command()
        self.assertEqual(command[1:], ["-m", "autoapply", "bridge"])

    def test_a_plain_script_is_started_the_way_it_was(self):
        with patch("autoapply.service.sys.argv", ["/usr/local/bin/autoapply", "bridge"]):
            command = service._self_command()
        self.assertEqual(command[1:], ["/usr/local/bin/autoapply", "bridge"])


class RunningUnderServiceTests(unittest.TestCase):
    def test_systemd_calling_the_unit_active_counts(self):
        active = subprocess.CompletedProcess([], 0, "active\n", "")
        with patch("autoapply.service.current_platform", return_value="linux"), \
             patch("autoapply.service.subprocess.run", return_value=active):
            self.assertTrue(service.running_under_service())

    def test_an_inactive_unit_does_not(self):
        inactive = subprocess.CompletedProcess([], 3, "inactive\n", "")
        with patch("autoapply.service.current_platform", return_value="linux"), \
             patch("autoapply.service.subprocess.run", return_value=inactive):
            self.assertFalse(service.running_under_service())

    def test_a_service_manager_that_is_not_there_is_not_an_error(self):
        with patch("autoapply.service.current_platform", return_value="macos"), \
             patch("autoapply.service.subprocess.run",
                   side_effect=FileNotFoundError("launchctl")):
            self.assertFalse(service.running_under_service())


# ── Building throwaway repositories to update ────────────────────────────────

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True,
        env={**os.environ,
             "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.com",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.com",
             "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull},
    )


def _commit(repo: Path, name: str, text: str) -> None:
    (repo / name).write_text(text)
    _git(repo, "add", name)
    _git(repo, "commit", "-m", f"add {name}")


def _repo(path: Path) -> Path:
    path.mkdir(parents=True)
    _git(path, "init", "-b", "main")
    _commit(path, "seed.txt", "seed")
    return path


def _origin_and_clone(root: Path) -> tuple[Path, Path]:
    origin = _repo(root / "origin")
    clone = root / "clone"
    subprocess.run(["git", "clone", "--quiet", str(origin), str(clone)],
                   capture_output=True, text=True)
    _git(clone, "config", "user.email", "test@example.com")
    _git(clone, "config", "user.name", "test")
    return origin, clone
