import unittest
from workforce.identity_key_officer import CredentialMetadata, propose_key_action

class IdentityKeyOfficerTests(unittest.TestCase):
    def setUp(self):
        self.meta = CredentialMetadata("github-deploy", "tenant-a", "github", "bot-020",
                                       "vault://tenant-a/github-deploy")

    def test_metadata_only(self):
        self.assertEqual(self.meta.status, "requested")
        self.assertNotIn("secret", str(propose_key_action(self.meta, "rotate", "bot-020")).lower())

    def test_no_plaintext_reference(self):
        with self.assertRaises(ValueError):
            CredentialMetadata("key", "tenant-a", "github", "bot-020", "ghp_plaintext")

    def test_separation_of_duties(self):
        with self.assertRaises(ValueError):
            propose_key_action(self.meta, "approve", "bot-020", "bot-020")

    def test_unknown_operation(self):
        with self.assertRaises(ValueError):
            propose_key_action(self.meta, "export_all_secrets", "bot-020")

if __name__ == "__main__":
    unittest.main()
