from __future__ import annotations

import ast
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLACES_SCRIPT = REPOSITORY_ROOT / "scripts" / "places.py"


def load_places_module():
    spec = importlib.util.spec_from_file_location("places_script", PLACES_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


places = load_places_module()


class PlacesStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.home = Path(self.temporary.name) / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_state_files_are_created_but_never_replaced_by_setup(self) -> None:
        manual, generated = places.ensure_state_files(self.home)
        manual.write_text("work = ~/work\n", encoding="utf-8")
        generated.write_text("/existing/repository\n", encoding="utf-8")

        places.ensure_state_files(self.home)

        self.assertEqual(manual.read_text(encoding="utf-8"), "work = ~/work\n")
        self.assertEqual(generated.read_text(encoding="utf-8"), "/existing/repository\n")

    def test_manual_format_is_validated_with_actionable_examples(self) -> None:
        manual, _ = places.ensure_state_files(self.home)
        manual.write_text("not valid\n", encoding="utf-8")
        with self.assertRaisesRegex(
            places.PlacesError, r"places\.txt:1: expected 'alias = path'.*core = ~"
        ):
            places.load_favorites(manual)

        manual.write_text("123 = ~/work\n", encoding="utf-8")
        with self.assertRaisesRegex(places.PlacesError, "aliases must start with a letter"):
            places.load_favorites(manual)

        manual.write_text("work = relative/path\n", encoding="utf-8")
        with self.assertRaisesRegex(places.PlacesError, "absolute or start with '~'"):
            places.load_favorites(manual)

    def test_manual_aliases_preserve_file_order_and_are_case_insensitive(self) -> None:
        first = self.home / "first"
        second = self.home / "second"
        first.mkdir()
        second.mkdir()
        manual, _ = places.ensure_state_files(self.home)
        manual.write_text(
            "Zulu = {}\nalpha = {}\n".format(first, second), encoding="utf-8"
        )

        favorites = places.load_favorites(manual)

        self.assertEqual([alias for alias, _ in favorites], ["Zulu", "alpha"])
        manual.write_text(
            "Core = {}\ncore = {}\n".format(first, second), encoding="utf-8"
        )
        with self.assertRaisesRegex(places.PlacesError, "aliases are case-insensitive"):
            places.load_favorites(manual)


class PlacesDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.home = Path(self.temporary.name) / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_refresh_discovers_git_directories_and_worktree_files_deterministically(self) -> None:
        zulu = self.home / "work" / "zulu"
        alpha = self.home / "work" / "alpha"
        ignored = self.home / "work" / "node_modules" / "ignored"
        (zulu / ".git").mkdir(parents=True)
        alpha.mkdir(parents=True)
        (alpha / ".git").write_text("gitdir: elsewhere\n", encoding="utf-8")
        (ignored / ".git").mkdir(parents=True)

        repositories, errors = places.refresh([], self.home)

        self.assertEqual(errors, [])
        self.assertEqual(repositories, [alpha.resolve(), zulu.resolve()])
        generated = places.state_paths(self.home)[1]
        self.assertEqual(
            generated.read_text(encoding="utf-8").splitlines(),
            [str(alpha.resolve()), str(zulu.resolve())],
        )

    def test_extra_roots_are_scanned_and_invalid_root_preserves_cache(self) -> None:
        outside = Path(self.temporary.name) / "outside" / "repo"
        (outside / ".git").mkdir(parents=True)
        _, generated = places.ensure_state_files(self.home)
        generated.write_text("original\n", encoding="utf-8")

        with self.assertRaisesRegex(places.PlacesError, "Scan root is not"):
            places.refresh([str(Path(self.temporary.name) / "missing")], self.home)
        self.assertEqual(generated.read_text(encoding="utf-8"), "original\n")

        repositories, _ = places.refresh([str(outside.parent)], self.home)
        self.assertEqual(repositories, [outside.resolve()])

    def test_favorite_wins_over_duplicate_generated_repository(self) -> None:
        repository = self.home / "work" / "repo"
        (repository / ".git").mkdir(parents=True)
        manual, generated = places.ensure_state_files(self.home)
        manual.write_text("main = {}\n".format(repository), encoding="utf-8")
        generated.write_text("{}\n".format(repository.resolve()), encoding="utf-8")

        favorites, repositories = places.load_places(self.home)

        self.assertEqual(favorites, [("main", repository.resolve())])
        self.assertEqual(repositories, [])


class PlacesMenuTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.home = Path(self.temporary.name) / "home"
        favorite = self.home / "favorite"
        repository = self.home / "work" / "repository"
        favorite.mkdir(parents=True)
        repository.mkdir(parents=True)
        manual, generated = places.ensure_state_files(self.home)
        manual.write_text("core = {}\n".format(favorite), encoding="utf-8")
        generated.write_text("{}\n".format(repository), encoding="utf-8")
        self.favorite = favorite.resolve()
        self.repository = repository.resolve()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_menu_has_separate_stable_aliases_and_generated_numbers(self) -> None:
        favorites, repositories = places.load_places(self.home)
        menu = places.render_menu(favorites, repositories, self.home.resolve())
        self.assertIn("Favorites (1)", menu)
        self.assertIn("[core]", menu)
        self.assertIn("Git repositories (1)", menu)
        self.assertIn("[1]", menu)
        self.assertLess(menu.index("Favorites"), menu.index("Git repositories"))

    def test_choose_accepts_alias_or_number_and_reprompts_on_invalid_input(self) -> None:
        menu = io.StringIO()
        with patch("sys.stdout", new_callable=io.StringIO):
            selected = places.choose(
                self.home,
                input_stream=io.StringIO("wrong\nCORE\n"),
                menu_stream=menu,
            )
        self.assertEqual(selected, self.favorite)
        self.assertIn("Invalid selection", menu.getvalue())

        output = Path(self.temporary.name) / "selection.txt"
        selected = places.choose(
            self.home,
            input_stream=io.StringIO("1\n"),
            menu_stream=io.StringIO(),
            selection_file=output,
        )
        self.assertEqual(selected, self.repository)
        self.assertEqual(output.read_text(encoding="utf-8").strip(), str(self.repository))


class PlacesInstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.home = Path(self.temporary.name) / "home"
        self.home.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_linux_install_is_idempotent_and_preserves_state(self) -> None:
        manual = self.home / ".agent-core" / places.MANUAL_FILENAME
        generated = self.home / ".agent-core" / places.GENERATED_FILENAME
        manual.parent.mkdir()
        manual.write_text("keep = {}\n".format(self.home), encoding="utf-8")
        generated.write_text("keep generated\n", encoding="utf-8")

        first = places.install(
            source=PLACES_SCRIPT,
            home=self.home,
            platform="linux",
            python_executable=Path("/usr/bin/python3"),
        )
        second = places.install(
            source=PLACES_SCRIPT,
            home=self.home,
            platform="linux",
            python_executable=Path("/usr/bin/python3"),
        )

        self.assertTrue(first["bashrc_changed"])
        self.assertFalse(second["bashrc_changed"])
        self.assertEqual(manual.read_text(encoding="utf-8"), "keep = {}\n".format(self.home))
        self.assertEqual(generated.read_text(encoding="utf-8"), "keep generated\n")
        self.assertEqual((self.home / ".bashrc").read_text().count(places.BASH_BLOCK_BEGIN), 1)
        function = first["function"].read_text(encoding="utf-8")
        self.assertIn("builtin cd --", function)
        self.assertIn("choose", function)

    def test_windows_launcher_changes_drive_and_directory(self) -> None:
        launcher = places._render_cmd_launcher(
            Path("C:/Python/python.exe"),
            Path("C:/Users/Test/AppData/Local/Places/places.py"),
            Path("C:/Users/Test/AppData/Local/Places"),
        )
        self.assertIn("cd /d", launcher)
        self.assertIn("choose --selection-file", launcher)
        self.assertIn(":run_command", launcher)

    @unittest.skipUnless(os.name == "nt", "requires Windows CMD")
    def test_installed_cmd_launcher_changes_its_calling_shell_directory(self) -> None:
        target = self.home / "favorite"
        target.mkdir()
        local = Path(self.temporary.name) / "local"
        with patch.object(places, "add_to_windows_user_path", return_value=False):
            result = places.install(
                source=PLACES_SCRIPT,
                home=self.home,
                platform="windows",
                python_executable=Path(sys.executable),
                local_app_data=local,
            )
        places.state_paths(self.home)[0].write_text(
            "core = {}\n".format(target), encoding="utf-8"
        )
        answer = Path(self.temporary.name) / "answer.txt"
        answer.write_text("core\n", encoding="utf-8")
        driver = Path(self.temporary.name) / "driver.cmd"
        driver.write_text(
            '@echo off\r\ncd /d "{}"\r\ncall "{}" < "{}"\r\ncd\r\n'.format(
                self.home, result["launcher"], answer
            ),
            encoding="utf-8",
        )
        environment = os.environ.copy()
        environment.update({"HOME": str(self.home), "USERPROFILE": str(self.home)})

        completed = subprocess.run(
            ["cmd.exe", "/d", "/c", str(driver)],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(Path(completed.stdout.strip()).resolve(), target.resolve())

    @unittest.skipUnless(os.name == "posix", "requires Bash on a POSIX host")
    def test_installed_bash_function_changes_its_calling_shell_directory(self) -> None:
        target = self.home / "favorite"
        target.mkdir()
        result = places.install(
            source=PLACES_SCRIPT,
            home=self.home,
            platform="linux",
            python_executable=Path(sys.executable),
        )
        places.state_paths(self.home)[0].write_text(
            "core = {}\n".format(target), encoding="utf-8"
        )
        answer = Path(self.temporary.name) / "answer.txt"
        answer.write_text("core\n", encoding="utf-8")
        command = 'source "{}"; cd "{}"; places < "{}"; pwd'.format(
            result["bashrc"], self.home, answer
        )
        environment = os.environ.copy()
        environment["HOME"] = str(self.home)

        completed = subprocess.run(
            ["bash", "-c", command],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(Path(completed.stdout.strip()).resolve(), target.resolve())

    def test_source_remains_python_38_compatible(self) -> None:
        ast.parse(
            PLACES_SCRIPT.read_text(encoding="utf-8"),
            filename=str(PLACES_SCRIPT),
            feature_version=(3, 8),
        )


if __name__ == "__main__":
    unittest.main()
