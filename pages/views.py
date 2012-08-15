from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_protect

from .models import Page
from .utils import get_site_id


@csrf_protect
def page(request, url_path):
    site_id = get_site_id(request)
    queryset = Page.objects.published()
    queryset = queryset.filter(sites=site_id, language=get_language())
    page = get_object_or_404(queryset, url_path=url_path)
    return render(request, 'pages/%s' % page.template, {
        'page': page,
    })
