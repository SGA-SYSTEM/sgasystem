# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from sistema_sga.prova.models import UsuarioProva
from django.contrib.auth import authenticate, login as django_login, logout as django_logout


def home(request):
    print request.user.id
    return render(request, 'core/home.html')