from django.urls import path
from .views import home, about, api_lab, contact, resume_download, contact_submit

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("api-lab/", api_lab, name="api-lab"),
    path("contact/", contact, name="contact"),
    path("resume/download/", resume_download, name="resume-download"),
    path("contact/send/", contact_submit, name="contact-send"),
]
