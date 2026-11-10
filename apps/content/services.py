from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from .models import ContactMessage, Resume, SiteProfile, SiteSettings


def singleton(model):
    """Return the first record for admin-managed single-record content models."""
    obj = model.objects.first()
    return obj


def send_contact_message(data):
    """Persist a contact submission and send a notification email when configured."""
    msg = ContactMessage.objects.create(**data)
    send_mail(
        data.get("subject") or f'Portfolio message from {data["name"]}',
        f'From: {data["name"]} <{data["email"]}>\n\n{data["message"]}',
        settings.DEFAULT_FROM_EMAIL,
        [settings.CONTACT_EMAIL],
        fail_silently=True,
    )
    return msg


def active_resume():
    """Return the most recently uploaded resume marked active."""
    return Resume.objects.filter(is_active=True).order_by("-uploaded_at").first()
