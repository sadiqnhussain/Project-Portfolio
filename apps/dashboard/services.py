import time
from urllib.error import URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

from django.core.cache import cache
from django.db import connection
from django.utils import timezone

from .models import ServiceProbe


def _probe_database():
    """Measure database connectivity with a minimal read-only query."""
    started = time.perf_counter()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return {
            "name": "Database",
            "status": "healthy",
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }
    except Exception:
        return {
            "name": "Database",
            "status": "down",
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }


def _probe_cache():
    """Verify that the configured cache can store and retrieve a short-lived value."""
    started = time.perf_counter()
    key = "portfolio_health_probe"
    try:
        cache.set(key, "ok", timeout=10)
        healthy = cache.get(key) == "ok"
        return {
            "name": "Cache",
            "status": "healthy" if healthy else "degraded",
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }
    except Exception:
        return {
            "name": "Cache",
            "status": "down",
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }


def _probe_application():
    """Report application-process availability without making a recursive request."""
    started = time.perf_counter()
    try:
        # The health service itself is executing inside Django, so this measures
        # application execution rather than making a recursive HTTP request.
        status = "healthy"
    except Exception:
        status = "down"
    return {
        "name": "Django / API",
        "status": status,
        "latency_ms": max(0, round((time.perf_counter() - started) * 1000)),
    }


def _probe_static_storage():
    """Check whether a representative static asset can be located."""
    started = time.perf_counter()
    try:
        from django.contrib.staticfiles import finders

        healthy = bool(finders.find("css/base.css"))
        return {
            "name": "Static Assets",
            "status": "healthy" if healthy else "degraded",
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }
    except Exception:
        return {
            "name": "Static Assets",
            "status": "degraded",
            "latency_ms": round((time.perf_counter() - started) * 1000),
        }


def _probe_url(url, timeout_ms=3000):
    """Request a configured health URL and return status, latency, HTTP code, and error."""
    started = time.perf_counter()
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return "down", 0, None, "Health URL must use http or https."
        request = Request(
            url, headers={"User-Agent": "PortfolioSite-HealthMonitor/1.0"}, method="GET"
        )
        with urlopen(request, timeout=max(timeout_ms, 250) / 1000) as response:
            status_code = response.status
        latency = round((time.perf_counter() - started) * 1000)
        status = "healthy" if 200 <= status_code < 400 else "degraded"
        return status, latency, status_code, ""
    except (URLError, TimeoutError, OSError) as exc:
        return (
            "down",
            round((time.perf_counter() - started) * 1000),
            None,
            str(exc)[:160],
        )
    except Exception as exc:
        return (
            "down",
            round((time.perf_counter() - started) * 1000),
            None,
            str(exc)[:160],
        )


def build_health_snapshot(projects=None):
    """Build a live snapshot of local services and enabled project monitors."""
    services = [
        _probe_application(),
        _probe_database(),
        _probe_cache(),
        _probe_static_storage(),
    ]
    monitored = []
    for project in projects or []:
        url = project.health_check_url or project.live_url
        if not url or not project.health_check_enabled:
            continue
        status, latency, status_code, error = _probe_url(
            url, project.health_check_timeout_ms
        )
        monitored.append(
            {
                "id": project.id,
                "slug": project.slug,
                "title": project.title,
                "url": url,
                "status": status,
                "latency_ms": latency,
                "http_status": status_code,
                "error": error,
            }
        )

    service_statuses = [item["status"] for item in services]
    overall = (
        "down"
        if any(s == "down" for s in service_statuses)
        else "degraded" if any(s == "degraded" for s in service_statuses) else "healthy"
    )
    return {
        "overall": overall,
        "generated_at": timezone.now(),
        "services": services,
        "projects": monitored,
    }


def seed_default_probes():
    # Kept for backwards compatibility with existing installations. Health is
    # now measured live and no longer reads dashboard-entered latency values.
    return ServiceProbe.objects.count()
