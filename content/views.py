import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseGone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET

from . import site_data
from .forms import ContactForm
from .models import FAQ, Article, CaseStudy, Category, Service

logger = logging.getLogger(__name__)


def cached(view):
    """Keep the finished page in memory for a few minutes (only on the live server)."""
    seconds = settings.PAGE_CACHE_SECONDS
    return cache_page(seconds)(view) if seconds else view


@require_GET
@cached
def home(request):
    return render(request, "content/home.html", {
        "services": Service.objects.all(),
        "articles": Article.published.select_related("category")[:3],
        "case_studies": CaseStudy.objects.all()[:3],
        "process_steps": site_data.PROCESS_STEPS,
        "testimonials": site_data.TESTIMONIALS,
    })


@require_GET
@cached
def about(request):
    return render(request, "content/about.html", {
        "core_values": site_data.CORE_VALUES,
        "differentiators": site_data.DIFFERENTIATORS,
        "process_steps": site_data.PROCESS_STEPS,
        "services": Service.objects.all(),
    })


@require_GET
@cached
def service_list(request):
    return render(request, "content/service_list.html", {"services": Service.objects.all()})


@require_GET
@cached
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, "content/service_detail.html", {
        "service": service,
        "other_services": Service.objects.exclude(pk=service.pk),
    })


@require_GET
@cached
def casestudy_list(request):
    return render(request, "content/casestudy_list.html", {"case_studies": CaseStudy.objects.all()})


@require_GET
@cached
def casestudy_detail(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug)
    return render(request, "content/casestudy_detail.html", {
        "case": case,
        "other_cases": CaseStudy.objects.exclude(pk=case.pk)[:3],
    })


@require_GET
@cached
def article_list(request, category_slug=None):
    articles = Article.published.select_related("category")
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        articles = articles.filter(category=category)
    page = Paginator(articles, 9).get_page(request.GET.get("page"))
    return render(request, "content/article_list.html", {
        "page": page,
        "category": category,
        "categories": Category.objects.filter(articles__isnull=False).distinct(),
    })


@require_GET
@cached
def article_detail(request, slug):
    article = get_object_or_404(Article.published.select_related("category"), slug=slug)
    return render(request, "content/article_detail.html", {
        "article": article,
        "recent": Article.published.exclude(pk=article.pk)[:3],
    })


@require_GET
@cached
def faq(request):
    return render(request, "content/faq.html", {"faqs": FAQ.objects.all()})


@require_GET
@cached
def privacy(request):
    return render(request, "content/privacy.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            try:
                send_mail(
                    subject=f"[Website] {msg.subject}",
                    message=(f"From: {msg.name} <{msg.email}>\nPhone: {msg.phone}\n\n{msg.message}"),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception:  # the message is saved in the admin anyway
                logger.exception("Could not email contact message %s", msg.pk)
            messages.success(request, "Thank you! Your message has been sent. We will reply soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "content/contact.html", {"form": form})


# --- Old WordPress addresses ------------------------------------------------------

def legacy_article(request, year, month, day, slug):
    """Old article links looked like /2025/07/23/slug/. Send visitors to the new page.

    Addresses that don't match a real article were spam posted by hackers: answer
    "410 Gone" so Google removes them from its results quickly.
    """
    article = Article.published.filter(slug=slug).first()
    if article:
        return redirect(article, permanent=True)
    return HttpResponseGone("This page has been permanently removed.")


def legacy_service(request, slug):
    service = Service.objects.filter(slug=slug).first()
    return redirect(service or "service_list", permanent=True)


def legacy_casestudy(request, slug):
    case = CaseStudy.objects.filter(slug=slug).first()
    return redirect(case or "casestudy_list", permanent=True)


def gone(request, *args, **kwargs):
    return HttpResponseGone("This page has been permanently removed.")


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /manage-ws/",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
