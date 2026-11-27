from django.urls import path, re_path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.service_list, name="service_list"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("case-studies/", views.casestudy_list, name="casestudy_list"),
    path("case-studies/<slug:slug>/", views.casestudy_detail, name="casestudy_detail"),
    path("blog/", views.article_list, name="article_list"),
    path("blog/category/<slug:category_slug>/", views.article_list, name="article_category"),
    path("blog/<slug:slug>/", views.article_detail, name="article_detail"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),

    # ----- Old WordPress addresses (keep links from Google and other sites working) -----
    re_path(r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/?$",
            views.legacy_article),
    path("service/<slug:slug>/", views.legacy_service),
    path("portfolio/<slug:slug>/", views.legacy_casestudy),
    path("about-us/", RedirectView.as_view(pattern_name="about", permanent=True)),
    path("contact-us/", RedirectView.as_view(pattern_name="contact", permanent=True)),
    path("privacy-policy-2/", RedirectView.as_view(pattern_name="privacy", permanent=True)),
    path("our-team/", RedirectView.as_view(pattern_name="about", permanent=True)),
    path("pricing/", RedirectView.as_view(pattern_name="contact", permanent=True)),
    # WordPress files that robots keep trying; tell them they are gone for good
    re_path(r"^(wp-login\.php|xmlrpc\.php|wp-admin/.*|wp-content/.*|wp-includes/.*|feed/?)$",
            views.gone),
]
