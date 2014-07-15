# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'^system/$', 'sistema_sga.prova.views.usuario_prova', name='usuario_prova'),
    url(r'^$', 'sistema_sga.core.views.home', name='home'),
    url(r'^prova/', include('sistema_sga.prova.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
