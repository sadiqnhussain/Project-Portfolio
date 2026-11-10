"""Integration tests for API documentation and key public routes."""

from django.test import TestCase


class APIDocumentationTests(TestCase):
    """Ensure the OpenAPI schema and interactive documentation are reachable."""

    def test_schema_endpoint_returns_openapi_document(self):
        response = self.client.get("/schema/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("openapi", response.json())

    def test_swagger_and_redoc_pages_load(self):
        for endpoint in ("/docs/", "/redoc/"):
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                self.assertEqual(response.status_code, 200)


class PublicPageSmokeTests(TestCase):
    """Check that the primary public pages remain routable."""

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_project_index_loads(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 200)
