# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth.decorators import login_required
from .views import ProfileView

admin.autodiscover()

urlpatterns = patterns('sistema_sga.profiles.views',
                       url(r'^settings/$', login_required
                           (ProfileView.as_view()), name='profile'),
                       )
