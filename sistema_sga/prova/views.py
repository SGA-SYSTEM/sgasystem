# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect, redirect
from sistema_sga.prova.models import Prova, UsuarioProva, Questao, Resposta, UsuarioProvaResposta
from django.utils import timezone
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
from sistema_sga.prova.forms import ProvaForm, QuestaoForm

# Create your views here.

@login_required
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
    context = { 'usuario_prova':usuario_prova, }
    return HttpResponseRedirect('/home-sga/')

@login_required
def enviar_prova(request, prova_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        if usuario_prova.get_progress() == '100%':
            if not usuario_prova.tempo_final:
                usuario_prova.tempo_final = timezone.now()
                usuario_prova.save()
                messages.add_message(request, messages.SUCCESS, 'Prova enviada!')
                return HttpResponseRedirect('/home-sga/')
            else:
                messages.add_message(request, messages.ERROR, 'Prova em andamento.')
        else:
            messages.add_message(request, messages.ERROR, 'É preciso responder todas as questões.')
    else:
        messages.add_message(request, messages.ERROR, 'Usuário sem permissão.')
    return HttpResponseRedirect('/home-sga/')

@login_required
def prova(request, prova_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        context = { 'usuario_prova':usuario_prova }
        return render(request, 'prova/provas.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Usuário sem permissão.')
        return HttpResponseRedirect('/')

@login_required
def questao(request, prova_id, questao_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        questao = Questao.objects.get(pk=questao_id)
        respostas = Resposta.objects.filter(questao__id=questao_id).order_by('id')
        try:
            usuario_resposta = UsuarioProvaResposta.objects.get(usuario_prova__id=prova_id, questao__id=questao_id)
        except:
            usuario_resposta = None
    context = {'usuario_prova':usuario_prova, 'questao':questao, 
               'respostas':respostas, 'usuario_resposta':usuario_resposta,
            }
    return render(request, 'prova/questao.html', context)

@login_required
def send_response(request):
    if request.method == 'POST':
        usuario_prova_id = request.POST['user-exam-id']
        questao_id = request.POST['question-id']
        resposta_id = request.POST['rb-answer']
        usuario_prova_resposta = UsuarioProvaResposta.objects.filter(usuario_prova__id=usuario_prova_id, questao__id=questao_id)
        usuario_prova_resposta.delete()

        usuario_prova_resposta = UsuarioProvaResposta(usuario_prova=UsuarioProva(id=usuario_prova_id), questao=Questao(id=questao_id), resposta_alternativa=Resposta(id=resposta_id))
        usuario_prova_resposta.save()

        return HttpResponseRedirect('/home-sga/')

@login_required
def home_sga(request):
    usuario_prova_list = UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')
    context = {'usuario_prova_list':usuario_prova_list}
    return render(request, 'sga_system/home_sga.html', context)

@login_required
def desempenho(request):
    usuario_items = UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')
    lista = []
    for x in usuario_items:
        lista.append(x.get_score_for_pie())
    return render(request, 'prova/chart_graph.html', {
                            'usuario_items':usuario_items,'lista':lista,
                            })

#create exam for user
def create_exam(request):
    #do something... come on!
    return render(request, 'user_exam/create_exam_for_user.html', {
                            'form':ProvaForm(), 'form_question':QuestaoForm
                            })