"""Unit tests for the gated JAWE proposal scaffold."""
import unittest
from workforce.engine import propose_role, route_model, record_feedback

class WorkforceTests(unittest.TestCase):
    def test_role_proposal_requires_approval(self):
        role = propose_role("Build a website for a solo founder")
        self.assertEqual(role.name, "engineering-specialist")
        self.assertEqual(role.status, "pending_human_approval")
        self.assertFalse(role.execution_enabled)
        self.assertFalse(role.training_enabled)

    def test_duplicate_role_refused(self):
        with self.assertRaises(ValueError):
            propose_role("Build a website", ["engineering-specialist"])

    def test_router_restricted(self):
        self.assertEqual(route_model(["coding"], ["deepseek"]), "deepseek")
        with self.assertRaises(ValueError):
            route_model(["coding"], ["unknown"])

    def test_empty_allowlist_rejected(self):
        with self.assertRaises(ValueError):
            route_model(["coding"], [])

    def test_nan_feedback_rejected(self):
        with self.assertRaises(ValueError):
            record_feedback("test-002", True, float("nan"), 0.1)

    def test_feedback_training_opt_out(self):
        self.assertIn('"eligible_for_training": false', record_feedback("test-001", True, 0.9, 0.1))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            propose_role("x")

if __name__ == "__main__":
    unittest.main()
