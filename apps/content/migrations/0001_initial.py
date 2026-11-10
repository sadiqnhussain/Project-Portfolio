from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="SiteProfile",
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
                ("name", models.CharField(default="Your Name", max_length=120)),
                (
                    "role_label",
                    models.CharField(default="Backend Engineer", max_length=160),
                ),
                (
                    "headline",
                    models.CharField(
                        default="Building reliable backend systems.", max_length=220
                    ),
                ),
                ("short_bio", models.TextField(blank=True)),
                ("full_bio", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("github_url", models.URLField(blank=True)),
                ("linkedin_url", models.URLField(blank=True)),
                ("website_url", models.URLField(blank=True)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="profile/"),
                ),
                ("seo_title", models.CharField(blank=True, max_length=180)),
                ("seo_description", models.CharField(blank=True, max_length=320)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SiteSettings",
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
                (
                    "cta_title",
                    models.CharField(default="Let's build something.", max_length=180),
                ),
                (
                    "cta_text",
                    models.TextField(
                        default="Have a backend problem worth solving? Let’s build something reliable."
                    ),
                ),
                (
                    "cta_contact_label",
                    models.CharField(default="Contact me", max_length=60),
                ),
                (
                    "cta_email_label",
                    models.CharField(default="Email me", max_length=60),
                ),
                (
                    "resume_label",
                    models.CharField(default="Download resume", max_length=60),
                ),
                ("footer_text", models.CharField(blank=True, max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
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
                ("category", models.CharField(max_length=80)),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(blank=True, max_length=220)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Experience",
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
                ("role", models.CharField(max_length=140)),
                ("company", models.CharField(blank=True, max_length=140)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("is_current", models.BooleanField(default=False)),
                ("summary", models.TextField()),
                ("achievements", models.TextField(blank=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Recommendation",
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
                ("name", models.CharField(max_length=140)),
                ("job_title", models.CharField(max_length=140)),
                ("company", models.CharField(blank=True, max_length=140)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="recommendations/"
                    ),
                ),
                ("message", models.TextField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Resume",
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
                ("label", models.CharField(default="Resume", max_length=120)),
                ("file", models.FileField(upload_to="resumes/")),
                ("is_active", models.BooleanField(default=True)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="ResumeDownload",
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
                ("downloaded_at", models.DateTimeField(auto_now_add=True)),
                ("visitor_hash", models.CharField(blank=True, max_length=64)),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="downloads",
                        to="content.resume",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ContactMessage",
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
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(blank=True, max_length=180)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddIndex(
            model_name="resumedownload",
            index=models.Index(
                fields=["resume", "visitor_hash"],
                name="content_res_resume_i_7d1a0a_idx",
            ),
        ),
    ]
