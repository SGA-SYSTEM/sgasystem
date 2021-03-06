# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('sistema_sga.messages.views',
                       url(r'^$', 'inbox', name='inbox'),
                       url(r'^(?P<username>[^/]+)/$',
                           'messages', name='messages'),
                       url(r'^in/new/$', 'new', name='new_message'),
                       url(r'^in/send/$', 'send', name='send_message'),
                       url(r'^in/users/$', 'users', name='users_message'),
                       )
