import io
import json
import unittest
from workforce.open_source_radar import search_repositories, make_report

class FakeResponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): self.close()

class RadarTests(unittest.TestCase):
    def test_discovery_is_non_executable(self):
        def opener(request, timeout):
            self.assertIn("api.github.com", request.full_url)
            return FakeResponse(json.dumps({"items": [{
                "full_name": "example/project",
                "html_url": "https://github.com/example/project",
                "pushed_at": "2026-11-03T00:00:00Z",
                "stargazers_count": 42,
                "license": {"spdx_id": "Apache-2.0"},
                "description": "sample",
            }]}).encode())
        results = search_repositories(opener=opener)
        self.assertEqual(results[0]["status"], "research_only")
        self.assertTrue(results[0]["approval_required"])
        report = make_report("agents", results)
        self.assertFalse(report["automatic_code_changes"])
        self.assertFalse(report["automatic_deployment"])

    def test_invalid_inputs(self):
        for args in ({"topic": "unknown"}, {"since": "bad"}, {"limit": 100}):
            with self.assertRaises(ValueError):
                search_repositories(**args)

if __name__ == "__main__":
    unittest.main()
