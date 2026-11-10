from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("projects", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="project",
            name="health_check_url",
            field=models.URLField(
                blank=True,
                help_text="Optional endpoint to monitor; falls back to Live URL.",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="health_check_enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="project",
            name="health_check_timeout_ms",
            field=models.PositiveIntegerField(default=3000),
        ),
    ]
