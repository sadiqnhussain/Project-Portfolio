from django.contrib import admin
from .models import (
    SiteProfile,
    SiteSettings,
    Skill,
    Experience,
    Recommendation,
    Resume,
    ResumeDownload,
    ContactMessage,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role_label", "email", "updated_at")
    search_fields = ("name", "headline", "email")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "role_label",
                    "headline",
                    "short_bio",
                    "full_bio",
                    "location",
                    "email",
                    "avatar",
                )
            },
        ),
        ("Social", {"fields": ("github_url", "linkedin_url", "website_url")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("cta_title", "resume_label")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_published", "sort_order")
    list_filter = ("category", "is_published")
    search_fields = ("name", "category")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "role",
        "company",
        "start_date",
        "end_date",
        "is_current",
        "is_published",
    )
    list_filter = ("is_current", "is_published")
    search_fields = ("role", "company")


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("name", "job_title", "company", "is_published", "sort_order")
    list_filter = ("is_published",)
    search_fields = ("name", "job_title", "company", "message")


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "is_active",
        "uploaded_at",
        "downloads_total",
        "downloads_unique",
    )
    list_filter = ("is_active",)
    readonly_fields = ("uploaded_at", "downloads_total", "downloads_unique")

    @admin.display(description="Total downloads")
    def downloads_total(self, obj):
        return obj.total_downloads

    @admin.display(description="Unique downloads (approx.)")
    def downloads_unique(self, obj):
        return obj.unique_downloads


@admin.register(ResumeDownload)
class ResumeDownloadAdmin(admin.ModelAdmin):
    list_display = ("resume", "downloaded_at", "visitor_hash")
    readonly_fields = ("resume", "downloaded_at", "visitor_hash")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
