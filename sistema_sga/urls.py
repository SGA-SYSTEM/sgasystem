	# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.flatpages.views import flatpage

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'^pages/(?P<url>.*/)$', flatpage, name='flatpage'),
    url(r'^dashboard/$', 'sistema_sga.prova.views.dashboard', name='dashboard'),
    url(r'^$', 'sistema_sga.core.views.home', name='home'),
    url(r'^in/(?P<username>[^/]+)/$', 'sistema_sga.core.views.profile', name='my_profile'),
    url(r'^prova/', include('sistema_sga.prova.urls')),
    url(r'^profile/', include('sistema_sga.core.urls')),
    url(r'^messages/', include('sistema_sga.messages.urls')),
    url(r'^rede/', 'sistema_sga.core.views.rede', name='network'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
