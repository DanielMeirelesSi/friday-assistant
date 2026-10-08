from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
DOCUMENTATION = ROOT / "references" / "capabilities" / "documentation"
CAPABILITY = DOCUMENTATION / "capability.md"
WORKFLOWS = DOCUMENTATION / "workflows"
MIGRATED_PATHS = (
    "references/capabilities/documentation/documentation-standard.md",
    "references/capabilities/documentation/documentation-writing.md",
    "references/capabilities/documentation/evidence-and-trust.md",
    "references/capabilities/documentation/repository-analysis.md",
    "references/capabilities/documentation/state-and-ownership.md",
    "references/capabilities/documentation/workflows/plan.md",
    "references/capabilities/documentation/workflows/generate.md",
    "references/capabilities/documentation/workflows/update.md",
    "references/capabilities/documentation/workflows/audit.md",
)
LEGACY_PATHS = (
    "references/documentation-standard.md",
    "references/documentation-writing.md",
    "references/evidence-and-trust.md",
    "references/repository-analysis.md",
    "references/state-and-ownership.md",
    "references/workflows/plan.md",
    "references/workflows/generate.md",
    "references/workflows/update.md",
    "references/workflows/audit.md",
)
WORKFLOW_PATHS = (
    "references/capabilities/documentation/workflows/plan.md",
    "references/capabilities/documentation/workflows/generate.md",
    "references/capabilities/documentation/workflows/update.md",
    "references/capabilities/documentation/workflows/audit.md",
)
DOCUMENTATION_REFERENCE_PATHS = (
    "references/capabilities/documentation/documentation-standard.md",
    "references/capabilities/documentation/documentation-writing.md",
    "references/capabilities/documentation/evidence-and-trust.md",
    "references/capabilities/documentation/repository-analysis.md",
    "references/capabilities/documentation/state-and-ownership.md",
)


class PlatformStructureTests(unittest.TestCase):
    def test_documentation_capability_entrypoint_is_selected_by_skill(self) -> None:
        self.assertTrue(CAPABILITY.is_file())
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/capabilities/documentation/capability.md", skill_text)
        self.assertEqual(skill_text.count("references/capabilities/documentation/"), 1)

        for workflow_path in WORKFLOW_PATHS:
            with self.subTest(path=workflow_path):
                self.assertNotIn(workflow_path, skill_text)

    def test_documentation_files_exist_only_at_capability_paths(self) -> None:
        for path in MIGRATED_PATHS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())

        for path in LEGACY_PATHS:
            with self.subTest(path=path):
                self.assertFalse((ROOT / path).exists())

    def test_capability_references_migrated_workflows_and_documentation(self) -> None:
        capability_text = CAPABILITY.read_text(encoding="utf-8")

        for path in (*WORKFLOW_PATHS, *DOCUMENTATION_REFERENCE_PATHS):
            with self.subTest(path=path):
                self.assertIn(path, capability_text)

    def test_documentation_workflow_directory_has_all_workflows(self) -> None:
        for workflow in ("plan.md", "generate.md", "update.md", "audit.md"):
            with self.subTest(workflow=workflow):
                self.assertTrue((WORKFLOWS / workflow).is_file())


if __name__ == "__main__":
    unittest.main()
