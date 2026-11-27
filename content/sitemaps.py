from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article, CaseStudy, Service


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["home", "about", "service_list", "casestudy_list", "article_list", "faq", "contact"]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.published_at


class ServiceSitemap(Sitemap):
    changefreq = "yearly"

    def items(self):
        return Service.objects.all()


class CaseStudySitemap(Sitemap):
    changefreq = "yearly"

    def items(self):
        return CaseStudy.objects.all()


SITEMAPS = {
    "pages": StaticSitemap,
    "articles": ArticleSitemap,
    "services": ServiceSitemap,
    "case-studies": CaseStudySitemap,
}
