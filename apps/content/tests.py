"""Regression tests for public portfolio content API endpoints."""

from rest_framework.test import APITestCase


class PublicContentAPITests(APITestCase):
    """Verify public content endpoints respond without requiring visitor accounts."""

    def test_empty_profile_returns_object(self):
        response = self.client.get("/api/v1/content/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_public_collection_endpoints_return_success(self):
        for endpoint in (
            "/api/v1/content/skills/",
            "/api/v1/content/experience/",
            "/api/v1/content/recommendations/",
        ):
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                self.assertEqual(response.status_code, 200)
                self.assertIsInstance(response.json(), list)

    def test_about_endpoint_returns_expected_sections(self):
        response = self.client.get("/api/v1/content/about/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json()), {"profile", "skills", "experience", "recommendations"}
        )
