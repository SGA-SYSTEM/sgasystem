# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from sistema_sga.prova.models import UsuarioProva
from django.conf import settings

from django.views.generic import View
from django.core.urlresolvers import reverse as r
from .forms import ProfileForm
from django.utils.translation import ugettext as _

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives

def home(request):
    print request.user.id
    return render(request, 'core/home.html')
"""
@receiver(user_signed_up)
def set_attribute(sender, **kwargs):
    user = kwargs.pop('user')
    try:
        extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    except Exception:
        extra_data = None
    if extra_data is not None:
        social_link = extra_data['link'] 
        name = extra_data['name'] 
        first_name = extra_data['first_name'] 
        last_name = extra_data['last_name'] 
        email = extra_data['email'] 

        user.facebook_link = social_link
        user.name = name
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        #try to send welcome email
        subject = 'Bem vindo ao TôBuscando!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]
        to = email
        text_content = 'Something...'
        html_content = render_to_string(
            'welcome.html', {'equipe':'tobuscando'}
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        subject = 'Bem vindo!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email, settings.EMAIL_HOST_USER]
        to = user.email
        text_content = 'Something...'
        html_content = render_to_string(
            'welcome.html', {'equipe':'sga'}
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       
        msg.attach_alternative(html_content, "text/html")
        msg.send()
"""

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

@receiver(user_signed_up)
def set_attribute(sender, **kwargs):
    user = kwargs.pop('user')
    try:
        extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    except Exception:
        extra_data = None
    if extra_data is not None:
        social_link = extra_data['link'] 
        name = extra_data['name'] 
        first_name = extra_data['first_name'] 
        last_name = extra_data['last_name'] 
        email = extra_data['email'] 
        language = extra_data['locale'] 
        if language == 'pt_BR':
            user.language = u'Português' 
            user.country = 'Brasil' 
        else: 
            user.language = language

        user.social_link_fc = social_link
        user.name = name
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        #try to send welcome email
        subject = 'Sistema S.G.A'
        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]
        to = email
        text_content = 'A description...'
        html_content = render_to_string(
            'account/email/email_confirmation_message.html', {'equipe':'sga'}
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        subject = 'Sistema S.G.A'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email, settings.EMAIL_HOST_USER]
        to = user.email
        text_content = 'A description...'
        html_content = render_to_string(
            'account/email/email_confirmation_message.html', {'equipe':'sga'}
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       
        msg.attach_alternative(html_content, "text/html")
        msg.send()
