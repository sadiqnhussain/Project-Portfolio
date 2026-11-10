from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Technology",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=80, unique=True)),
                ("category", models.CharField(blank=True, max_length=60)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=160)),
                ("slug", models.SlugField(unique=True)),
                ("summary", models.TextField()),
                ("full_description", models.TextField(blank=True)),
                ("architecture", models.TextField(blank=True)),
                ("achievements", models.TextField(blank=True)),
                ("challenges", models.TextField(blank=True)),
                ("solutions", models.TextField(blank=True)),
                ("category", models.CharField(blank=True, max_length=80)),
                ("stack", models.JSONField(blank=True, default=list)),
                (
                    "cover_image",
                    models.ImageField(blank=True, null=True, upload_to="projects/"),
                ),
                (
                    "architecture_diagram",
                    models.ImageField(
                        blank=True, null=True, upload_to="projects/architecture/"
                    ),
                ),
                ("repository_url", models.URLField(blank=True)),
                ("live_url", models.URLField(blank=True)),
                ("documentation_url", models.URLField(blank=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_recent", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="technologies",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="projects.technology"
            ),
        ),
    ]
