# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from sistema_sga.prova.models import UsuarioProva
from django.views.generic import View
from django.core.urlresolvers import reverse as r
from .forms import ProfileForm
from django.utils.translation import ugettext as _


def home(request):
    print request.user.id
    return render(request, 'core/home.html')

class ProfileView(View):
    template_name = 'profile/profile.html'
    form_class = ProfileForm
    success_message = _(u'Dados alterados com sucesso.')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES,
                               instance=request.user)

        if form.is_valid():
            profile = form.save()

            messages.success(request, self.success_message)
            return HttpResponseRedirect('/profile/data/')

        return render(request, self.template_name, locals())