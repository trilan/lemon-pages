from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from publications.admin import PublicationAdmin

from .forms import PageAdminForm
from .models import Page


if 'lemon' in settings.INSTALLED_APPS:
    import lemon as admin
else:
    from django.contrib import admin


if 'metadata' in settings.INSTALLED_APPS:
    import metadata
    MetadataAdminMixin = metadata.MetadataAdminMixin
else:
    class MetadataAdminMixin(object):
        pass


class PageAdmin(MetadataAdminMixin, PublicationAdmin):

    form = PageAdminForm
    date_hierarchy = None
    search_fields = ['title', 'content']
    markup_fields = ('content',)
    fieldsets = (
        (None, {
            'fields': (
                'url_path', 'title', 'content', 'template', 'language',
                'sites',
            )
        }),
    ) + PublicationAdmin.fieldsets
    list_display = ('url_path', 'title', 'language')
    list_display_links = ('title',)
    list_filter = ('enabled', 'language', 'sites')
    string_overrides = {
        'add_title': _(u'Add page'),
        'change_title': _(u'Change page'),
        'changelist_title': _(u'Choose page to change'),
        'changelist_popup_title': _(u'Choose page'),
        'changelist_addlink_title': _(u'Add page'),
        'changelist_paginator_description': lambda n: \
            ungettext(u'%(count)d page', u'%(count)d pages', n)
    }
    tabs = True


admin.site.register(Page, PageAdmin)

if 'metadata' in settings.INSTALLED_APPS:
    metadata.site.register(Page,
        language_field_name='language',
        sites_field_name='sites'
    )
