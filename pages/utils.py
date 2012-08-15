from django.conf import settings
from django.contrib.sites.models import Site


def get_site_id(request):
    if hasattr(request, 'site') and isinstance(request.site, Site):
        return request.site.id
    try:
        return Site.objects.get(id=settings.SITE_ID).id
    except Site.DoesNotExist:
        return None
