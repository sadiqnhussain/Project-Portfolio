"""Regression tests for project listing and detail API behavior."""

from rest_framework.test import APITestCase


class ProjectAPITests(APITestCase):
    """Verify public project API behavior with an empty project catalog."""

    def test_project_list_returns_collection(self):
        response = self.client.get("/api/v1/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_missing_project_detail_returns_not_found(self):
        response = self.client.get("/api/v1/projects/no-such-project/")
        self.assertEqual(response.status_code, 404)

    def test_missing_project_health_returns_not_found(self):
        response = self.client.get("/api/v1/projects/no-such-project/health/")
        self.assertEqual(response.status_code, 404)
