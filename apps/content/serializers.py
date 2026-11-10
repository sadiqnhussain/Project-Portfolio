from rest_framework import serializers
from .models import SiteProfile, SiteSettings, Skill, Experience, Recommendation, Resume


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProfile
        fields = "__all__"


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    total_downloads = serializers.IntegerField(read_only=True)
    unique_downloads = serializers.IntegerField(read_only=True)

    class Meta:
        model = Resume
        fields = ["id", "label", "uploaded_at", "total_downloads", "unique_downloads"]
