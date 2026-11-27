from django.contrib import admin

from .models import FAQ, Article, CaseStudy, Category, ContactMessage, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published")
    list_filter = ("is_published", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (None, {"fields": ["title", "slug", "icon", "order", "summary"]}),
        ("The story (challenge, journey, outcome)", {
            "description": "Each service page tells a short client story in three chapters.",
            "fields": ["headline", "challenge", "journey", "outcome"],
        }),
        ("What's included", {"fields": ["body"]}),
    ]


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "categories", "published_at")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    actions = ["mark_read"]

    @admin.action(description="Mark selected messages as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
