from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.services import build_health_snapshot
from .models import Project
from .services import project_queryset
from .serializers import ProjectSerializer


class ProjectListAPIView(ListAPIView):
    """List published projects with optional featured and recent filters."""

    serializer_class = ProjectSerializer

    def get_queryset(self):
        def flag(k):
            v = self.request.query_params.get(k)
            return None if v is None else v.lower() in ("1", "true", "yes")

        return project_queryset(flag("featured"), flag("recent"))


class ProjectDetailAPIView(RetrieveAPIView):
    """Return the published case study for a project slug."""

    queryset = Project.objects.filter(is_published=True).prefetch_related(
        "technologies"
    )
    serializer_class = ProjectSerializer
    lookup_field = "slug"


class ProjectHealthAPIView(APIView):
    """Return health information for a published project."""

    def get(self, request, slug):
        project = Project.objects.filter(is_published=True, slug=slug).first()
        if not project:
            return Response({"detail": "Project not found."}, status=404)
        snapshot = build_health_snapshot([project])
        return Response(
            snapshot["projects"][0]
            if snapshot["projects"]
            else {
                "id": project.id,
                "title": project.title,
                "url": project.health_check_url or project.live_url,
                "status": "not_configured",
                "latency_ms": None,
                "http_status": None,
                "error": "Add a live URL or health-check URL in Admin.",
            }
        )


class SandboxTriggerAPIView(APIView):
    """Return the API Lab workflow simulation for a project identifier."""

    def post(self, request, pk):
        return Response(
            {
                "project_id": pk,
                "steps": [
                    {
                        "step": "request_received",
                        "status": "passed",
                        "detail": "Request accepted by API boundary.",
                    },
                    {
                        "step": "validation",
                        "status": "passed",
                        "detail": "Payload validated before business logic.",
                    },
                    {
                        "step": "service_layer",
                        "status": "passed",
                        "detail": "Business operation delegated to service layer.",
                    },
                    {
                        "step": "response_serialization",
                        "status": "passed",
                        "detail": "Result serialized for the client.",
                    },
                ],
                "response": {
                    "status": "completed",
                    "message": "Sandbox workflow executed successfully.",
                },
                "duration_ms": 12,
            }
        )
