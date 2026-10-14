import unittest
from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "VPe04: GitHub Actions + Docker")
        self.assertNotIn("environment", response.json)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_unknown_route(self):
        self.assertEqual(self.client.get("/unknown").status_code, 404)


if __name__ == "__main__":
    unittest.main()
