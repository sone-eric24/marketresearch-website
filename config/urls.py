from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_control
from django.views.static import serve

from content.sitemaps import SITEMAPS
from content.views import robots_txt

admin.site.site_header = "WS Market Research – Admin"
admin.site.site_title = "WS Market Research"

urlpatterns = [
    # A less obvious address for the admin makes automated login attacks harder
    path("manage-ws/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    # Uploaded images. On a small site Django can serve them itself; browsers
    # keep them for 30 days so returning visitors don't download them again.
    re_path(
        r"^media/(?P<path>.*)$",
        cache_control(max_age=60 * 60 * 24 * 30, public=True)(serve),
        {"document_root": settings.MEDIA_ROOT},
    ),
    path("", include("content.urls")),
]
