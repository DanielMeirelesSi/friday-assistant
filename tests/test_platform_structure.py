from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
CAPABILITY = ROOT / "references" / "capabilities" / "documentation" / "capability.md"
LEGACY_DOCUMENTATION_PATHS = (
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
    "references/workflows/plan.md",
    "references/workflows/generate.md",
    "references/workflows/update.md",
    "references/workflows/audit.md",
)


class PlatformStructureTests(unittest.TestCase):
    def test_documentation_capability_entrypoint_is_selected_by_skill(self) -> None:
        self.assertTrue(CAPABILITY.is_file())
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/capabilities/documentation/capability.md", skill_text)

        for workflow_path in WORKFLOW_PATHS:
            with self.subTest(path=workflow_path):
                self.assertNotIn(workflow_path, skill_text)

    def test_capability_owns_workflow_and_legacy_reference_routing(self) -> None:
        capability_text = CAPABILITY.read_text(encoding="utf-8")

        for path in (*WORKFLOW_PATHS, *LEGACY_DOCUMENTATION_PATHS):
            with self.subTest(path=path):
                self.assertIn(path, capability_text)

    def test_batch_one_keeps_legacy_documentation_references_in_place(self) -> None:
        for path in LEGACY_DOCUMENTATION_PATHS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())


if __name__ == "__main__":
    unittest.main()
