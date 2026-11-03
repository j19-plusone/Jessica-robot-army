import unittest
from workforce.security_shield import Principal, authorize, default_new_role

class ShieldTests(unittest.TestCase):
    def test_new_role_is_restricted(self):
        bot = default_new_role("new-001", "tenant-a")
        self.assertTrue(authorize(bot, "propose_upgrade", "tenant-a").allowed)
        self.assertFalse(authorize(bot, "deploy", "tenant-a", approval=True).allowed)

    def test_cross_tenant_denied(self):
        bot = Principal("bot", "tenant-a", frozenset({"read_public_repo"}))
        self.assertEqual(authorize(bot, "read_public_repo", "tenant-b").reason, "cross_tenant_denied")

    def test_approval_and_sandbox(self):
        bot = Principal("bot", "tenant-a", frozenset({"model_training"}))
        self.assertFalse(authorize(bot, "model_training", "tenant-a").allowed)
        self.assertFalse(authorize(bot, "model_training", "tenant-a", approval=True).allowed)
        self.assertTrue(authorize(bot, "model_training", "tenant-a", approval=True, sandbox=True).allowed)

    def test_unknown_action_fails_closed(self):
        bot = Principal("bot", "tenant-a", frozenset({"admin_everything"}))
        self.assertFalse(authorize(bot, "admin_everything", "tenant-a", approval=True).allowed)

if __name__ == "__main__":
    unittest.main()
