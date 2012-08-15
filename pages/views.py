from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_protect

from .models import Page


@csrf_protect
def page(request, url_path):
    queryset = Page.objects.published()
    queryset = queryset.filter(sites=request.site, language=get_language())
    page = get_object_or_404(queryset, url_path=url_path)
    return TemplateResponse(request, 'pages/%s' % page.template, {
        'page': page,
    })
