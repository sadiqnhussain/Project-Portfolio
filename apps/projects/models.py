from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=80, unique=True)
    category = models.CharField(max_length=60, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    full_description = models.TextField(blank=True)
    architecture = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    solutions = models.TextField(blank=True)
    category = models.CharField(max_length=80, blank=True)
    stack = models.JSONField(default=list, blank=True)
    technologies = models.ManyToManyField(
        Technology, blank=True, related_name="projects"
    )
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    architecture_diagram = models.ImageField(
        upload_to="projects/architecture/", blank=True, null=True
    )
    repository_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    health_check_url = models.URLField(
        blank=True, help_text="Optional endpoint to monitor; falls back to Live URL."
    )
    health_check_enabled = models.BooleanField(default=True)
    health_check_timeout_ms = models.PositiveIntegerField(default=3000)
    is_featured = models.BooleanField(default=False)
    is_recent = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def tech_names(self):
        return (
            list(
                self.technologies.filter(is_active=True)
                .order_by("sort_order", "name")
                .values_list("name", flat=True)
            )
            or self.stack
        )
