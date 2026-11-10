from django.urls import path
from .api_views import (
    ProjectListAPIView,
    ProjectDetailAPIView,
    ProjectHealthAPIView,
    SandboxTriggerAPIView,
)

urlpatterns = [
    path("", ProjectListAPIView.as_view()),
    path("<slug:slug>/", ProjectDetailAPIView.as_view()),
    path("<slug:slug>/health/", ProjectHealthAPIView.as_view()),
    path("<int:pk>/sandbox-trigger/", SandboxTriggerAPIView.as_view()),
]
