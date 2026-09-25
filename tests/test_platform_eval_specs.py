from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLATFORM_CASES = ROOT / "tests" / "evals" / "platform_cases.json"


class PlatformEvalSpecTests(unittest.TestCase):
    def test_platform_cases_are_well_formed(self) -> None:
        cases = json.loads(PLATFORM_CASES.read_text(encoding="utf-8"))
        self.assertIsInstance(cases, list)
        self.assertTrue(cases)

        valid_dispositions = {"route", "unsupported", "clarify"}
        valid_workflows = {"plan", "generate", "update", "audit"}
        ids: set[str] = set()

        for case in cases:
            with self.subTest(case=case.get("id")):
                self.assertIsInstance(case, dict)
                self.assertIsInstance(case.get("id"), str)
                self.assertTrue(case["id"].strip())
                self.assertNotIn(case["id"], ids)
                ids.add(case["id"])

                self.assertIsInstance(case.get("request"), str)
                self.assertTrue(case["request"].strip())
                self.assertIn("expected_capability", case)
                self.assertIn(case.get("expected_disposition"), valid_dispositions)
                assertions = case.get("manual_assertions")
                self.assertIsInstance(assertions, list)
                self.assertTrue(assertions)
                self.assertTrue(all(isinstance(item, str) and item.strip() for item in assertions))

                disposition = case["expected_disposition"]
                if disposition == "route":
                    self.assertEqual(case["expected_capability"], "documentation")
                    self.assertIn(case.get("expected_workflow"), valid_workflows)
                elif disposition == "unsupported":
                    self.assertIsInstance(case["expected_capability"], str)
                    self.assertTrue(case["expected_capability"].strip())
                    self.assertNotEqual(case["expected_capability"], "documentation")
                    self.assertNotIn("expected_workflow", case)
                else:
                    self.assertIsNone(case["expected_capability"])
                    self.assertNotIn("expected_workflow", case)

    def test_platform_disposition_coverage(self) -> None:
        cases = json.loads(PLATFORM_CASES.read_text(encoding="utf-8"))
        dispositions = {case["expected_disposition"] for case in cases}
        self.assertTrue({"route", "unsupported", "clarify"}.issubset(dispositions))

        unsupported_capabilities = {
            case["expected_capability"]
            for case in cases
            if case["expected_disposition"] == "unsupported"
        }
        self.assertTrue({"architecture", "testing", "security"}.issubset(unsupported_capabilities))


if __name__ == "__main__":
    unittest.main()
