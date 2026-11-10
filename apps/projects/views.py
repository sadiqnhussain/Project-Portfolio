from django.shortcuts import render


def projects_page(request):
    return render(request, "projects/projects.html")


def project_detail_page(request, slug):
    return render(request, "projects/project_detail.html", {"project_slug": slug})


def sandbox_page(request):
    return render(request, "projects/sandbox.html")
