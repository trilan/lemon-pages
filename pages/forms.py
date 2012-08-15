from django import forms
from django.contrib.sites.models import Site
from django.db.models import Count, Max
from django.utils.translation import ugettext_lazy as _

from .models import Page
from .widgets import SelectPageTemplate


class PageAdminForm(forms.ModelForm):

    url_path = forms.RegexField(
        label=_(u'URL path'),
        max_length=255,
        regex=r'^/[\.\-/\w]*$',
        error_messages={
            'invalid': _(
                u'Enter a valid URL path beginning with slash and consisting '
                u'of letters, numbers, underscores, slashes or hyphens.'
            ),
        },
    )
    template = forms.CharField(
        label=_(u'Template'),
        max_length=255,
        widget=SelectPageTemplate(),
        error_messages={
            'required': _(u'Please create template for pages'),
        },
    )

    def is_url_path_unique(self):
        queryset = Site.objects.filter(
            pk__in=self.cleaned_data['sites'],
            page__url_path=self.cleaned_data['url_path'],
            page__language=self.cleaned_data['language'],
        )
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(page__pk=self.instance.pk)
        queryset = queryset.annotate(page_count=Count('page'))
        result = queryset.aggregate(page_count_max=Max('page_count'))
        return not result['page_count_max']

    def clean(self):
        url_path = self.cleaned_data.get('url_path')
        sites = self.cleaned_data.get('sites')
        language = self.cleaned_data.get('language')
        if url_path and sites and language and not self.is_url_path_unique():
            msg = _(
                u'Page %s already exists for some of selected sites and '
                u'language'
            )
            raise forms.ValidationError(msg % url_path)
        return self.cleaned_data

    class Meta:
        model = Page
