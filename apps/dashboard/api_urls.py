from django.urls import path
from .api_views import HealthAPIView

urlpatterns = [path("dashboard/health/", HealthAPIView.as_view())]
