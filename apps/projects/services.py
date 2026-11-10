from .models import Project


def project_queryset(featured=None, recent=None):
    """Return published projects with related technologies and optional filters."""
    qs = (
        Project.objects.filter(is_published=True)
        .prefetch_related("technologies")
        .order_by("sort_order", "-created_at")
    )
    if featured is not None:
        qs = qs.filter(is_featured=featured)
    if recent is not None:
        qs = qs.filter(is_recent=recent)
    return qs
