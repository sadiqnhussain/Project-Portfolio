from django.urls import path
from .views import projects_page, project_detail_page, sandbox_page

urlpatterns = [
    path("", projects_page, name="projects"),
    path("sandbox/", sandbox_page, name="sandbox"),
    path("<slug:slug>/", project_detail_page, name="project-detail"),
]
