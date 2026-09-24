from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BEHAVIOR_CASES = ROOT / "tests" / "evals" / "behavior_cases.json"
ROUTING_CASES = ROOT / "tests" / "evals" / "routing_cases.json"
FIXTURES = ROOT / "tests" / "fixtures" / "behavior"
RUNNER = ROOT / "scripts" / "behavior_eval.py"


class BehaviorEvalSpecTests(unittest.TestCase):
    def test_behavior_cases_are_well_formed(self) -> None:
        cases = json.loads(BEHAVIOR_CASES.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 4)
        ids: set[str] = set()
        valid_workflows = {"plan", "generate", "update", "audit"}

        for case in cases:
            with self.subTest(case=case.get("id")):
                self.assertIsInstance(case.get("id"), str)
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])
                self.assertIn(case.get("expected_workflow"), valid_workflows)
                self.assertIsInstance(case.get("request"), str)
                self.assertTrue(case["request"].strip())
                fixture = FIXTURES / case["fixture"]
                self.assertTrue(fixture.is_dir(), fixture)
                self.assertFalse((fixture / ".git").exists())
                self.assertIsInstance(case.get("contract"), dict)
                post_baseline_changes = case.get("post_baseline_changes", {})
                self.assertIsInstance(post_baseline_changes, dict)
                for path, content in post_baseline_changes.items():
                    self.assertIsInstance(path, str)
                    self.assertIsInstance(content, str)
                    self.assertTrue((fixture / path).is_file(), path)

    def test_routing_cases_are_well_formed(self) -> None:
        cases = json.loads(ROUTING_CASES.read_text(encoding="utf-8"))
        expected_values = {"plan", "generate", "update", "audit", "clarify"}
        ids: set[str] = set()

        for case in cases:
            with self.subTest(case=case.get("id")):
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])
                self.assertIn(case["expected"], expected_values)
                self.assertTrue(case["request"].strip())

    def test_polling_fixtures_describe_exposed_interval(self) -> None:
        expected = "The poller module exposes a configured interval"
        for fixture_name in ("generate-idempotent", "update-minimal"):
            with self.subTest(fixture=fixture_name):
                fixture = FIXTURES / fixture_name
                documentation = (fixture / "docs" / "runtime.md").read_text(encoding="utf-8")
                state = json.loads((fixture / ".friday" / "state.json").read_text(encoding="utf-8"))

                self.assertIn(expected, documentation)
                self.assertNotIn("runs every", documentation)
                self.assertIn(expected, state["claims"][0]["claim"])

    def test_prepare_and_readonly_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "plan"
            prepare = subprocess.run(
                [sys.executable, str(RUNNER), "prepare", "plan-readonly", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(prepare.returncode, 0, prepare.stdout + prepare.stderr)
            self.assertTrue((workspace / ".git").is_dir())

            clean = subprocess.run(
                [sys.executable, str(RUNNER), "check", "plan-readonly", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

            (workspace / "src" / "config.js").write_text(
                "export const POLL_INTERVAL_MS = 99_000;\n", encoding="utf-8", newline="\n"
            )
            dirty = subprocess.run(
                [sys.executable, str(RUNNER), "check", "plan-readonly", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(dirty.returncode, 0)
            self.assertIn("requires a byte-for-byte clean result", dirty.stdout)

    def test_generate_checkpoint_defines_convergence_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "generate"
            prepare = subprocess.run(
                [sys.executable, str(RUNNER), "prepare", "generate-idempotent", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(prepare.returncode, 0, prepare.stdout + prepare.stderr)

            readme = workspace / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8") + "\nGenerated entry point details.\n",
                encoding="utf-8",
                newline="\n",
            )
            generated_doc = workspace / "docs" / "entry-point.md"
            generated_doc.write_text(
                "# Entry point\n\nThe public module entry point is documented here.\n",
                encoding="utf-8",
                newline="\n",
            )
            state_path = workspace / ".friday" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["documents"][0]["content_hash"] = "sha256:" + hashlib.sha256(readme.read_bytes()).hexdigest()
            state_path.write_text(
                json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            checkpoint = subprocess.run(
                [sys.executable, str(RUNNER), "checkpoint", "generate-idempotent", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(checkpoint.returncode, 0, checkpoint.stdout + checkpoint.stderr)

            meta_path = workspace.parent / f".{workspace.name}.friday-eval.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            self.assertNotEqual(meta["baseline"]["README.md"], meta["checkpoint"]["README.md"])
            self.assertEqual(meta["checkpoint"]["README.md"], hashlib.sha256(readme.read_bytes()).hexdigest())
            self.assertIn("docs/entry-point.md", meta["checkpoint"])

            stable = subprocess.run(
                [sys.executable, str(RUNNER), "check", "generate-idempotent", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(stable.returncode, 0, stable.stdout + stable.stderr)
            self.assertIn("Comparison: checkpoint", stable.stdout)
            self.assertIn("Changed paths: (none)", stable.stdout)

            checkpoint_readme = readme.read_bytes()
            readme.write_bytes(checkpoint_readme + b"\nUnexpected second-run change.\n")
            changed = subprocess.run(
                [sys.executable, str(RUNNER), "check", "generate-idempotent", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(changed.returncode, 0)
            self.assertIn("README.md", changed.stdout)

            readme.write_bytes(checkpoint_readme)
            restored = subprocess.run(
                [sys.executable, str(RUNNER), "check", "generate-idempotent", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)

    def test_update_checker_accepts_minimal_expected_diff(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir) / "update"
            prepare = subprocess.run(
                [sys.executable, str(RUNNER), "prepare", "update-minimal-diff", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(prepare.returncode, 0, prepare.stdout + prepare.stderr)

            config = workspace / "src" / "config.js"
            self.assertIn("POLL_INTERVAL_MS = 30_000", config.read_text(encoding="utf-8"))
            baseline_source = subprocess.run(
                ["git", "show", "HEAD:src/config.js"],
                cwd=workspace,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(baseline_source.returncode, 0, baseline_source.stderr)
            self.assertIn("POLL_INTERVAL_MS = 20_000", baseline_source.stdout)
            changed_paths = subprocess.run(
                ["git", "diff", "--name-only", "HEAD"],
                cwd=workspace,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(changed_paths.returncode, 0, changed_paths.stderr)
            self.assertEqual(
                changed_paths.stdout.splitlines(),
                ["src/config.js", "tests/poller.test.js"],
            )

            state = json.loads((workspace / ".friday" / "state.json").read_text(encoding="utf-8"))
            self.assertIn("20 seconds", state["claims"][0]["claim"])
            self.assertIn("20 seconds", (workspace / "docs" / "runtime.md").read_text(encoding="utf-8"))

            doc = workspace / "docs" / "runtime.md"
            doc.write_text(doc.read_text(encoding="utf-8").replace("20 seconds", "30 seconds"), encoding="utf-8", newline="\n")

            state_path = workspace / ".friday" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["claims"][0]["claim"] = "The poller module exposes a configured interval of 30 seconds."
            state["documents"][1]["content_hash"] = "sha256:" + hashlib.sha256(doc.read_bytes()).hexdigest()
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

            result = subprocess.run(
                [sys.executable, str(RUNNER), "check", "update-minimal-diff", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            (workspace / "README.md").write_text("unexpected rewrite\n", encoding="utf-8", newline="\n")
            forbidden = subprocess.run(
                [sys.executable, str(RUNNER), "check", "update-minimal-diff", "--workspace", str(workspace)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(forbidden.returncode, 0)
            self.assertIn("forbidden changed paths", forbidden.stdout)


if __name__ == "__main__":
    unittest.main()
