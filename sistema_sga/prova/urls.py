# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('sistema_sga.prova.views',
    url(r'^$', 'list_exam', name='list_exam'),
    url(r'^(?P<prova_id>\d+)/$', 'prova', name='prova'),
    url(r'^(?P<prova_id>\d+)/start/$', 'iniciar_prova', name='iniciar_prova'),
    url(r'^(?P<prova_id>\d+)/enviar/$', 'enviar_prova', name='enviar_prova'),
    url(r'^(?P<prova_id>\d+)/questao/(?P<questao_id>\d+)/$', 'questao'),
    url(r'^send-response/$', 'send_response'),
    url(r'^performance/$', 'performance', name='performance'),
    url(r'^overview/$', 'overview', name='overview'),
    #session user
    url(r'^criar_prova/$', 'create_exam', name='criar_prova'),
)