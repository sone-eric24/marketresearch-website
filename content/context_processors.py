from django.conf import settings


def site_info(request):
    """Makes the company details available in every template as {{ site.phone }} etc."""
    return {"site": settings.SITE_INFO}
