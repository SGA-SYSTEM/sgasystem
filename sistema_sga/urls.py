# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sistema_sga.core.views.home', name='home'),
    url(r'^prova/', include('sistema_sga.prova.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
