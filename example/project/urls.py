from django.conf.urls import patterns, include, url
from django.contrib import admin

from lemon import extradmin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(extradmin.site.urls)),
)
