# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from sistema_sga.prova.models import UsuarioProva
from sistema_sga.core.models import Profile
from sistema_sga.core.forms import ContactForm
from django.conf import settings
from django.views.generic import View
from django.core.urlresolvers import reverse as r
from .forms import ProfileForm
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives

from sistema_sga.prova.models import Prova, UsuarioProva
from django.db.models import Avg, Count, F, Max, Min, Sum, Q

def home(request):
    print request.user.id
    return render(request, 'core/home.html', {'form':ContactForm()})


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
            return HttpResponseRedirect('/profile/settings/')

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
        try:
            prova = Prova.objects.get(titulo='Teste')
            if prova:
                usuario_prova = UsuarioProva.objects.create(user=user, prova=prova, data_expiracao='2015-05-02')
                usuario_prova.save()
        except Exception, e:
            prova = None

@login_required
def rede(request):
    users = Profile.objects.filter(is_active=True).order_by('username')
    return render(request, 'core/rede.html', {'users': users,})

def profile(request, username):
    grid_user = get_object_or_404(Profile, username=username)
    query_user = UsuarioProva.objects.filter(user__id=grid_user.id)
    provas = Prova.objects.all().order_by('id')[0:5]
    titulos = list(set([u.titulo for u in provas]))
    try:
        query_data_user1 = UsuarioProva.objects.filter(user__username=username, prova__titulo=titulos[0])
        dump1 = max(list(set([i.get_score_for_pie() for i in query_data_user1])))
    except:
        dump1 = 0
    try:
        query_data_user2 = UsuarioProva.objects.filter(user__username=username, prova__titulo=titulos[1])
        dump2 = max(list(set([i.get_score_for_pie() for i in query_data_user2])))
    except:
        dump2 = 0
    try:
        query_data_user3 = UsuarioProva.objects.filter(user__username=username, prova__titulo=titulos[2])
        dump3 = max(list(set([i.get_score_for_pie() for i in query_data_user3])))
    except:
        dump3 = 0
    try:
        query_data_user4 = UsuarioProva.objects.filter(user__username=username, prova__titulo=titulos[3])
        dump4 = max(list(set([i.get_score_for_pie() for i in query_data_user4])))
    except:
        dump4 = 0
    try:
        query_data_user5 = UsuarioProva.objects.filter(user__username=username, prova__titulo=titulos[4])
        dump5 = max(list(set([i.get_score_for_pie() for i in query_data_user5])))
    except:
        dump5 = 0
    #for titulo in titulos:
    #    get_result = UsuarioProva.objects.filter(user__username=username, prova__titulo=titulo)[0:5]
    #    for i in get_result:
    #        if i.get_status() != 'Em Andamento':
    #            dump.append(i.get_score_for_pie())
    pending = len([p for p in query_user if p.get_status() != 'Finalizada!'])
    success = len([p for p in query_user if p.get_status() == 'Finalizada!'])
    context = {
        'grid_user': grid_user, 
        'username': username,
        'titulos': titulos,
        'score1': dump1,
        'score2': dump2,
        'score3': dump3,
        'score4': dump4,
        'score5': dump5,
        'pending': pending,
        'success': success,
    }
    return render(request, 'core/profile.html', context)

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid() and request.is_ajax():
        save_it = form.save(commit=False)
        save_it.save()
        subject = 'Obrigado por deixar sua opinião!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [save_it.email, settings.EMAIL_HOST_USER]
        to = save_it.email
        text_content = 'Obrigado por entrar em contato. Em breve teremos muitas novidades!'
        html_content = ""
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse("ok")
    return render(request, 'contact/contact.html')