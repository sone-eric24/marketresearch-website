import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(max_length=140, unique=True)),
            ],
            options={"verbose_name_plural": "categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="CaseStudy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("categories", models.CharField(blank=True, help_text="Comma-separated.", max_length=255)),
                ("summary", models.TextField(blank=True)),
                ("body", models.TextField(help_text="Case study text in HTML.")),
                ("featured_image", models.FileField(blank=True, upload_to="uploads/%Y/%m/")),
                ("published_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={"verbose_name_plural": "case studies", "ordering": ["-published_at"]},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("subject", models.CharField(max_length=150)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_read", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="FAQ",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=255)),
                ("answer", models.TextField(help_text="Answer in HTML.")),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"verbose_name": "FAQ", "verbose_name_plural": "FAQs", "ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("summary", models.TextField(blank=True, help_text="One or two sentences for the services list.")),
                ("body", models.TextField(help_text="Service description in HTML.")),
                ("order", models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")),
            ],
            options={"ordering": ["order", "title"]},
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("excerpt", models.TextField(blank=True, help_text="Short summary shown in the article list.")),
                ("meta_description", models.CharField(blank=True, help_text="Description shown by Google (about 155 characters).", max_length=300)),
                ("body", models.TextField(help_text="Article text in HTML.")),
                ("featured_image", models.FileField(blank=True, upload_to="uploads/%Y/%m/")),
                ("published_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_published", models.BooleanField(default=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="articles", to="content.category")),
            ],
            options={"ordering": ["-published_at"]},
        ),
    ]
