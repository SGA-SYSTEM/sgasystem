# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect, redirect, render_to_response
from sistema_sga.prova.models import Prova, UsuarioProva, Questao, Resposta, UsuarioProvaResposta
from django.utils import timezone
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
from sistema_sga.prova.forms import ProvaForm, QuestaoForm
from sistema_sga.core.models import Profile
from sistema_sga.decorators import ajax_required
import json

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
    return HttpResponseRedirect('/prova/')

@login_required
def enviar_prova(request, prova_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        if usuario_prova.get_progress() == '100%':
            if not usuario_prova.tempo_final:
                usuario_prova.tempo_final = timezone.now()
                usuario_prova.save()
                messages.add_message(request, messages.SUCCESS, 'Prova enviada!')
                return HttpResponseRedirect('/prova/')
            else:
                messages.add_message(request, messages.ERROR, 'Prova em andamento.')
        else:
            messages.add_message(request, messages.ERROR, 'É preciso responder todas as questões.')
    else:
        messages.add_message(request, messages.ERROR, 'Usuário sem permissão.')
    return HttpResponseRedirect('/prova/')

@login_required
def prova(request, prova_id):
    usuario_prova = UsuarioProva.objects.get(pk=prova_id)
    if request.user.id == usuario_prova.user.id:
        context = { 'usuario_prova':usuario_prova }
        return render(request, 'prova/provas.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Usuário sem permissão.')
        return HttpResponseRedirect('/accounts/login/')

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

        return HttpResponseRedirect('/prova/')

@login_required
def home_sga(request):
    usuario_prova_list = UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')
    try:
        exams_pending = len([x for x in UsuarioProva.objects.filter(user__id=request.user.id) if x.get_status() != 'Finalizada!'])
    except Exception, e:
        exams_pending = None
    context = {
    'usuario_prova_list': usuario_prova_list,
    'count_user': Profile.objects.all().count(),
    'exams_pending': exams_pending,
    'exams': Prova.objects.all().count(),
    'menu_progress': UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')[0:6]
    }
    return render(request, 'sga_system/home_sga.html', context)

@login_required
def performance(request):
    dump_query = UsuarioProva.objects.filter(user__id=request.user.id)
    try:
        query_median = UsuarioProva.objects.get(id=request.user.id)
        median_hit = query_median.get_median_score()
        median_errors = query_median.get_median_errors()
    except Exception, e:
        median_hit, median_errors = '0%', '0%'
    return render(request, 'chartit/chart.html', {
        'dump_query': dump_query,
        'menu_progress': UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')[0:6],
        'median_hit': median_hit,
        'median_errors': median_errors,
        })

#create exam for user
def create_exam(request):
    #do something... come on!
    return render(request, 'user_exam/create_exam_for_user.html', {
                            'form':ProvaForm(), 'form_question':QuestaoForm
                            })

# url 'list_exams'
def list_exam(request):
    usuario_prova_list = UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')
    context = {
    'usuario_prova_list':usuario_prova_list,
    'count_user':Profile.objects.all().count(),
    'menu_progress': UsuarioProva.objects.filter(user__id=request.user.id).order_by('id')[0:10]
    }
    return render(request, 'sga_system/list_exams.html', context)