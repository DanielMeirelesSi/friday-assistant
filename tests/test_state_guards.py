from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
STATE_CASES = json.loads((FIXTURES / "state_cases.json").read_text(encoding="utf-8"))
PYTHON_GUARD = ROOT / "scripts" / "state_guard.py"
POWERSHELL_GUARD = ROOT / "scripts" / "state_guard.ps1"
FIXTURE_REPO = FIXTURES / "repository"
FIXTURE_MANAGED_BYTES = b"Friday guard fixture managed document\n"


def find_powershell() -> str | None:
    for executable in ("pwsh", "powershell.exe", "powershell"):
        found = shutil.which(executable)
        if found:
            return found
    return None


POWERSHELL = find_powershell()
REQUIRE_POWERSHELL = os.environ.get("FRIDAY_REQUIRE_POWERSHELL") == "1"


def combined_output(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stdout + "\n" + result.stderr).lower()


def run_python(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PYTHON_GUARD), *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def run_powershell(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    if not POWERSHELL:
        raise RuntimeError("PowerShell is not available")

    command = [POWERSHELL, "-NoProfile"]
    if Path(POWERSHELL).name.lower().startswith("powershell"):
        command.extend(["-ExecutionPolicy", "Bypass"])
    command.extend(["-File", str(POWERSHELL_GUARD), *args])

    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def make_repo(parent: Path) -> Path:
    repo = parent / "repo"
    shutil.copytree(FIXTURE_REPO, repo)
    # Normalize the managed fixture bytes so hashes are platform-independent.
    (repo / "README.md").write_bytes(FIXTURE_MANAGED_BYTES)
    (repo / ".friday").mkdir(parents=True, exist_ok=True)
    return repo


def compact_valid_candidate() -> bytes:
    state = json.loads((FIXTURES / "states" / "valid-basic.json").read_text(encoding="utf-8"))
    # Deliberately non-canonical formatting. Install must preserve these exact bytes.
    return (json.dumps(state, ensure_ascii=False, separators=(",", ":")) + "\r\n").encode("utf-8")


class PythonGuardContractTests(unittest.TestCase):
    def test_validate_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = make_repo(Path(temp_dir))
            for case in STATE_CASES:
                with self.subTest(case=case["id"]):
                    state = FIXTURES / case["file"]
                    result = run_python(
                        "validate",
                        "--state",
                        str(state),
                        "--repo",
                        str(repo),
                    )
                    if case["valid"]:
                        self.assertEqual(result.returncode, 0, combined_output(result))
                    else:
                        self.assertNotEqual(result.returncode, 0, combined_output(result))
                        invariant = case.get("invariant")
                        if invariant and case["id"] != "invalid-json":
                            self.assertIn(invariant.lower(), combined_output(result))

    def test_install_preserves_candidate_bytes_and_resolves_paths_from_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = make_repo(temp)
            candidate = repo / ".friday" / "state.next.json"
            target = repo / ".friday" / "state.json"
            expected = compact_valid_candidate()
            candidate.write_bytes(expected)

            outside_cwd = temp / "outside-cwd"
            outside_cwd.mkdir()
            result = run_python(
                "install",
                "--candidate",
                ".friday/state.next.json",
                "--target",
                ".friday/state.json",
                "--repo",
                str(repo),
                cwd=outside_cwd,
            )

            self.assertEqual(result.returncode, 0, combined_output(result))
            self.assertEqual(target.read_bytes(), expected)
            self.assertEqual(list(target.parent.glob("state.json.*.tmp")), [])
            self.assertTrue(candidate.exists(), "guard must not remove the caller-owned candidate")

    def test_invalid_candidate_does_not_touch_live_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = make_repo(temp)
            candidate = repo / ".friday" / "state.next.json"
            target = repo / ".friday" / "state.json"
            candidate.write_bytes((FIXTURES / "states" / "unsupported-version.json").read_bytes())
            original = b"original live state bytes\n"
            target.write_bytes(original)

            result = run_python(
                "install",
                "--candidate",
                ".friday/state.next.json",
                "--target",
                ".friday/state.json",
                "--repo",
                str(repo),
            )

            self.assertNotEqual(result.returncode, 0, combined_output(result))
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(list(target.parent.glob("state.json.*.tmp")), [])


@unittest.skipUnless(POWERSHELL or REQUIRE_POWERSHELL, "PowerShell is not available")
class PowerShellGuardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if REQUIRE_POWERSHELL and not POWERSHELL:
            raise AssertionError("FRIDAY_REQUIRE_POWERSHELL=1 but no PowerShell executable was found")

    def test_validate_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = make_repo(Path(temp_dir))
            for case in STATE_CASES:
                with self.subTest(case=case["id"]):
                    state = FIXTURES / case["file"]
                    result = run_powershell(
                        "-Command",
                        "validate",
                        "-State",
                        str(state),
                        "-Repo",
                        str(repo),
                    )
                    if case["valid"]:
                        self.assertEqual(result.returncode, 0, combined_output(result))
                    else:
                        self.assertNotEqual(result.returncode, 0, combined_output(result))
                        invariant = case.get("invariant")
                        if invariant and case["id"] != "invalid-json":
                            self.assertIn(invariant.lower(), combined_output(result))

    def test_install_preserves_candidate_bytes_and_resolves_paths_from_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = make_repo(temp)
            candidate = repo / ".friday" / "state.next.json"
            target = repo / ".friday" / "state.json"
            expected = compact_valid_candidate()
            candidate.write_bytes(expected)

            outside_cwd = temp / "outside-cwd"
            outside_cwd.mkdir()
            result = run_powershell(
                "-Command",
                "install",
                "-Candidate",
                ".friday/state.next.json",
                "-Target",
                ".friday/state.json",
                "-Repo",
                str(repo),
                cwd=outside_cwd,
            )

            self.assertEqual(result.returncode, 0, combined_output(result))
            self.assertEqual(target.read_bytes(), expected)
            self.assertEqual(list(target.parent.glob("state.json.*.tmp")), [])
            self.assertTrue(candidate.exists(), "guard must not remove the caller-owned candidate")

    def test_invalid_candidate_does_not_touch_live_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = make_repo(temp)
            candidate = repo / ".friday" / "state.next.json"
            target = repo / ".friday" / "state.json"
            candidate.write_bytes((FIXTURES / "states" / "unsupported-version.json").read_bytes())
            original = b"original live state bytes\n"
            target.write_bytes(original)

            result = run_powershell(
                "-Command",
                "install",
                "-Candidate",
                ".friday/state.next.json",
                "-Target",
                ".friday/state.json",
                "-Repo",
                str(repo),
            )

            self.assertNotEqual(result.returncode, 0, combined_output(result))
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(list(target.parent.glob("state.json.*.tmp")), [])


@unittest.skipUnless(POWERSHELL or REQUIRE_POWERSHELL, "PowerShell is not available")
class GuardParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if REQUIRE_POWERSHELL and not POWERSHELL:
            raise AssertionError("FRIDAY_REQUIRE_POWERSHELL=1 but no PowerShell executable was found")

    def test_validate_verdict_parity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = make_repo(Path(temp_dir))
            for case in STATE_CASES:
                with self.subTest(case=case["id"]):
                    state = FIXTURES / case["file"]
                    py_result = run_python(
                        "validate",
                        "--state",
                        str(state),
                        "--repo",
                        str(repo),
                    )
                    ps_result = run_powershell(
                        "-Command",
                        "validate",
                        "-State",
                        str(state),
                        "-Repo",
                        str(repo),
                    )
                    self.assertEqual(
                        py_result.returncode == 0,
                        ps_result.returncode == 0,
                        "\n".join(
                            [
                                f"case: {case['id']}",
                                f"python: {combined_output(py_result)}",
                                f"powershell: {combined_output(ps_result)}",
                            ]
                        ),
                    )


if __name__ == "__main__":
    unittest.main()
