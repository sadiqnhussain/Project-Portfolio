from rest_framework.response import Response
from rest_framework.views import APIView
from apps.projects.models import Project
from .services import build_health_snapshot


class HealthAPIView(APIView):
    """Return live infrastructure and enabled project health checks."""

    def get(self, request):
        snapshot = build_health_snapshot(
            Project.objects.filter(is_published=True, health_check_enabled=True).only(
                "id",
                "slug",
                "title",
                "live_url",
                "health_check_url",
                "health_check_enabled",
                "health_check_timeout_ms",
            )
        )
        return Response(snapshot)
