from django.db import models


class ServiceProbe(models.Model):
    name = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=30, default="healthy")
    latency_ms = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
