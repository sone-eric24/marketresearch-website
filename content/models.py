"""
The website's content. Everything here can be edited in the admin
(http://yoursite/manage-ws/).

Fields called "body" hold HTML. Only trusted admin users can edit them.
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True, published_at__lte=timezone.now()
        )


class Article(models.Model):
    """A blog article / market insight."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="articles"
    )
    excerpt = models.TextField(blank=True, help_text="Short summary shown in the article list.")
    meta_description = models.CharField(
        max_length=300, blank=True, help_text="Description shown by Google (about 155 characters)."
    )
    body = models.TextField(help_text="Article text in HTML.")
    featured_image = models.FileField(upload_to="uploads/%Y/%m/", blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    objects = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])

    @property
    def reading_minutes(self):
        words = len(strip_tags(self.body).split())
        return max(1, round(words / 200))


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(blank=True, help_text="One or two sentences for the services list.")
    body = models.TextField(help_text="Service description in HTML.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.slug])


class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    categories = models.CharField(max_length=255, blank=True, help_text="Comma-separated.")
    summary = models.TextField(blank=True)
    body = models.TextField(help_text="Case study text in HTML.")
    featured_image = models.FileField(upload_to="uploads/%Y/%m/", blank=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "case studies"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("casestudy_detail", args=[self.slug])

    @property
    def category_list(self):
        return [c.strip() for c in self.categories.split(",") if c.strip()]


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text="Answer in HTML.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["order"]

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    """Messages sent through the contact form."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject}"
