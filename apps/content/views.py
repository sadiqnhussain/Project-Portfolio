import hashlib, secrets
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .models import Resume
from .services import active_resume, send_contact_message


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def api_lab(request):
    return render(request, "api_lab.html")


def contact(request):
    return render(request, "contact.html")


@require_GET
def resume_download(request):
    resume = active_resume()
    if not resume or not resume.file:
        raise Http404("No active resume")
    visitor = request.COOKIES.get("portfolio_visitor_id") or secrets.token_urlsafe(24)
    digest = hashlib.sha256(visitor.encode()).hexdigest()
    from .models import ResumeDownload

    ResumeDownload.objects.create(resume=resume, visitor_hash=digest)
    response = FileResponse(
        resume.file.open("rb"),
        as_attachment=True,
        filename=resume.file.name.rsplit("/", 1)[-1],
    )
    if not request.COOKIES.get("portfolio_visitor_id"):
        response.set_cookie(
            "portfolio_visitor_id",
            visitor,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="Lax",
        )
    return response


@require_POST
def contact_submit(request):
    data = {
        k: request.POST.get(k, "").strip()
        for k in ["name", "email", "subject", "message"]
    }
    if not data["name"] or not data["email"] or not data["message"]:
        return render(
            request,
            "contact.html",
            {"error": "Please complete your name, email, and message."},
            status=400,
        )
    send_contact_message(data)
    return render(
        request, "contact.html", {"success": "Thanks — your message has been sent."}
    )
