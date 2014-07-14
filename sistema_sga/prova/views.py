# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect, redirect
from sistema_sga.prova.models import Prova, UsuarioProva, Questao, Resposta
from django.utils import timezone
from django.contrib import messages
from django.template import RequestContext

# Create your views here.

def usuario_prova(request):
    usuario_prova_list = UsuarioProva.objects.filter(user__id=request.user.id).order_by('-id')
    context = {'usuario_prova_list':usuario_prova_list}
    return render(request, 'prova/usuarios_prova.html', context)

def iniciar_prova(request, prova_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        if not usuario_prova.has_expired():
            if not usuario_prova.tempo_inicial:
                usuario_prova.tempo_inicial = timezone.now()
                usuario_prova.save()
                return HttpResponseRedirect('/prova/%s/' %usuario_prova.id)
            else:
                messages.add_message(request, messages.ERROR, 'Esta prova já foi inicializada!')
        else:
            messages.add_message(request, messages.ERROR, 'Prova expirada.')
    else:
        messages.add_message(request, messages.ERROR, 'Usuário sem permissão.')
    context = {'usuario_prova':usuario_prova,}
    return HttpResponseRedirect('/')

def prova(request, prova_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        context = {'usuario_prova':usuario_prova}
        return render(request, 'prova/provas.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Usuário sem permissão.')
        return HttpResponseRedirect('/')

def questao(request, prova_id, questao_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        questao = Questao.objects.get(pk=questao_id)
        respostas = Resposta.objects.filter(questao__id=questao_id)
        try:
            usuario_resposta = UsuarioProvaResposta.objects.get(usuario_prova__id=prova_id, questao__id=questao_id)
        except:
            usuario_resposta = None
    context = {'usuario_prova':usuario_prova, 'questao':questao, 'respostas':respostas,}
    print context
    return render(request, 'prova/questao.html', context)