from django.urls import path
from .api_views import (
    ProfileAPIView,
    SiteAPIView,
    SkillsAPIView,
    ExperienceAPIView,
    RecommendationsAPIView,
    AboutAPIView,
)

urlpatterns = [
    path("profile/", ProfileAPIView.as_view()),
    path("site/", SiteAPIView.as_view()),
    path("skills/", SkillsAPIView.as_view()),
    path("experience/", ExperienceAPIView.as_view()),
    path("recommendations/", RecommendationsAPIView.as_view()),
    path("about/", AboutAPIView.as_view()),
]
