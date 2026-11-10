from django.db import models


class SiteProfile(models.Model):
    name = models.CharField(max_length=120, default="Your Name")
    role_label = models.CharField(max_length=160, default="Backend Engineer")
    headline = models.CharField(
        max_length=220, default="Building reliable backend systems."
    )
    short_bio = models.TextField(blank=True)
    full_bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=320, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    cta_title = models.CharField(max_length=180, default="Let's build something.")
    cta_text = models.TextField(
        default="Have a backend problem worth solving? Let’s build something reliable."
    )
    cta_contact_label = models.CharField(max_length=60, default="Contact me")
    cta_email_label = models.CharField(max_length=60, default="Email me")
    resume_label = models.CharField(max_length=60, default="Download resume")
    footer_text = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return "Site settings"


class Skill(models.Model):
    category = models.CharField(max_length=80)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=220, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    role = models.CharField(max_length=140)
    company = models.CharField(max_length=140, blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    summary = models.TextField()
    achievements = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "-start_date")

    def __str__(self):
        return f"{self.role} — {self.company}"


class Recommendation(models.Model):
    name = models.CharField(max_length=140)
    job_title = models.CharField(max_length=140)
    company = models.CharField(max_length=140, blank=True)
    photo = models.ImageField(upload_to="recommendations/", blank=True, null=True)
    message = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Resume(models.Model):
    label = models.CharField(max_length=120, default="Resume")
    file = models.FileField(upload_to="resumes/")
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_downloads(self):
        return self.downloads.count()

    @property
    def unique_downloads(self):
        return self.downloads.values("visitor_hash").distinct().count()

    def __str__(self):
        return self.label


class ResumeDownload(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="downloads"
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)
    visitor_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        indexes = [models.Index(fields=["resume", "visitor_hash"])]


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'{self.name} — {self.subject or "No subject"}'
