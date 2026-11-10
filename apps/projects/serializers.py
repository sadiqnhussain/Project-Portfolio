from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    tech_stack = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    architecture_diagram_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "full_description",
            "architecture",
            "achievements",
            "challenges",
            "solutions",
            "category",
            "tech_stack",
            "cover_image_url",
            "architecture_diagram_url",
            "repository_url",
            "live_url",
            "documentation_url",
            "health_check_url",
            "health_check_enabled",
            "is_featured",
            "is_recent",
        ]

    def get_tech_stack(self, obj):
        return obj.tech_names()

    def get_cover_image_url(self, obj):
        return obj.cover_image.url if obj.cover_image else None

    def get_architecture_diagram_url(self, obj):
        return obj.architecture_diagram.url if obj.architecture_diagram else None
