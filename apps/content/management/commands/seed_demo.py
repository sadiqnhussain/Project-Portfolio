from django.core.management.base import BaseCommand
from apps.content.models import (
    SiteProfile,
    SiteSettings,
    Skill,
    Experience,
    Recommendation,
)
from apps.projects.models import Project, Technology
from apps.dashboard.models import ServiceProbe
from datetime import date


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        SiteProfile.objects.get_or_create(
            pk=1,
            defaults={
                "name": "Your Name",
                "role_label": "Backend Engineer",
                "headline": "I design reliable APIs, data workflows, and production-ready backend systems.",
                "short_bio": "Backend engineer focused on Django, APIs, data, infrastructure, and pragmatic system design.",
                "full_bio": "Write your complete professional profile here. Explain your engineering approach, the kinds of systems you enjoy building, and the impact you aim to create.",
                "email": "you@example.com",
            },
        )
        SiteSettings.objects.get_or_create(pk=1)
        for name, cat in [
            ("Django", "Backend"),
            ("Django REST Framework", "Backend"),
            ("PostgreSQL", "Data"),
            ("Redis", "Infrastructure"),
            ("Docker", "Infrastructure"),
            ("Python", "Backend"),
            ("JavaScript", "Frontend"),
        ]:
            Technology.objects.get_or_create(name=name, defaults={"category": cat})
        for cat, names in {
            "Backend": ["Python", "Django", "Django REST Framework", "API Design"],
            "Data": ["PostgreSQL", "Data Modeling", "ETL"],
            "Infrastructure": ["Docker", "Redis", "CI/CD"],
        }.items():
            for i, n in enumerate(names):
                Skill.objects.get_or_create(
                    category=cat, name=n, defaults={"sort_order": i}
                )
        Experience.objects.get_or_create(
            role="Backend Engineer",
            company="Your Company",
            start_date=date(2024, 1, 1),
            defaults={
                "summary": "Describe the systems you built, operated, and improved.",
                "is_current": True,
            },
        )
        for n in ["API Gateway", "Queue", "PostgreSQL", "Cache"]:
            ServiceProbe.objects.get_or_create(name=n, defaults={"latency_ms": 10})
        for title, slug in [
            ("FromInto API", "frominto-api"),
            ("Async Job Monitor", "async-job-monitor"),
            ("Data Pipeline Lab", "data-pipeline-lab"),
        ]:
            p, _ = Project.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "summary": "A demonstration project showing clean backend architecture and operational thinking.",
                    "category": "Backend Systems",
                    "is_featured": True,
                    "is_recent": True,
                    "stack": ["Python", "Django", "PostgreSQL"],
                },
            )
            if p.technologies.count() == 0:
                p.technologies.set(
                    Technology.objects.filter(
                        name__in=["Python", "Django", "PostgreSQL"]
                    )
                )
        self.stdout.write(self.style.SUCCESS("Demo content ready."))
