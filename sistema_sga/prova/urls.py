# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('sistema_sga.prova.views',
    url(r'^$', 'prova', name='provas'),
)