from django.contrib import admin
from .models import Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "sort_order")
    list_filter = ("category", "is_active")
    search_fields = ("name", "category")
    ordering = ("sort_order", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_featured",
        "is_recent",
        "is_published",
        "sort_order",
        "updated_at",
    )
    list_filter = ("is_featured", "is_recent", "is_published", "category")
    search_fields = ("title", "summary", "full_description", "category")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "summary",
                    "full_description",
                    "category",
                    "cover_image",
                )
            },
        ),
        (
            "Engineering",
            {
                "fields": (
                    "architecture",
                    "achievements",
                    "challenges",
                    "solutions",
                    "architecture_diagram",
                    "technologies",
                    "stack",
                )
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "repository_url",
                    "live_url",
                    "documentation_url",
                    "health_check_url",
                    "health_check_enabled",
                    "health_check_timeout_ms",
                )
            },
        ),
        (
            "Publishing",
            {"fields": ("is_featured", "is_recent", "is_published", "sort_order")},
        ),
    )
