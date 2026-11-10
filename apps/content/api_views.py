from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SiteProfile, SiteSettings, Skill, Experience, Recommendation
from .serializers import (
    ProfileSerializer,
    SiteSerializer,
    SkillSerializer,
    ExperienceSerializer,
    RecommendationSerializer,
)


class ProfileAPIView(APIView):
    """Return the public profile record when one is configured."""

    def get(self, request):
        return Response(
            ProfileSerializer(SiteProfile.objects.first()).data
            if SiteProfile.objects.exists()
            else {}
        )


class SiteAPIView(APIView):
    """Return public site settings when a record is configured."""

    def get(self, request):
        return Response(
            SiteSerializer(SiteSettings.objects.first()).data
            if SiteSettings.objects.exists()
            else {}
        )


class SkillsAPIView(APIView):
    """List published skills in their configured display order."""

    def get(self, request):
        return Response(
            SkillSerializer(
                Skill.objects.filter(is_published=True).order_by(
                    "category", "sort_order", "name"
                ),
                many=True,
            ).data
        )


class ExperienceAPIView(APIView):
    """List published experience records."""

    def get(self, request):
        return Response(
            ExperienceSerializer(
                Experience.objects.filter(is_published=True), many=True
            ).data
        )


class RecommendationsAPIView(APIView):
    """List published recommendations in display order."""

    def get(self, request):
        return Response(
            RecommendationSerializer(
                Recommendation.objects.filter(is_published=True).order_by(
                    "sort_order", "name"
                ),
                many=True,
            ).data
        )


class AboutAPIView(APIView):
    """Return the profile and related public content in one response."""

    def get(self, request):
        return Response(
            {
                "profile": (
                    ProfileSerializer(SiteProfile.objects.first()).data
                    if SiteProfile.objects.exists()
                    else {}
                ),
                "skills": SkillSerializer(
                    Skill.objects.filter(is_published=True), many=True
                ).data,
                "experience": ExperienceSerializer(
                    Experience.objects.filter(is_published=True), many=True
                ).data,
                "recommendations": RecommendationSerializer(
                    Recommendation.objects.filter(is_published=True), many=True
                ).data,
            }
        )
