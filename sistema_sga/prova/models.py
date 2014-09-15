# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone
import datetime
from sistema_sga.core.models import Profile

# import user
from django.contrib.auth.models import User

class Prova(models.Model):
    titulo = models.CharField(_('titulo'), max_length=200, blank=True, null=False)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True, auto_now=False)
    sobre = models.ForeignKey('ProvaSobre')
    questoes = models.ManyToManyField('Questao', verbose_name=_('Questões'))
    duracao = models.IntegerField(_('Período'))

    class Meta:
        verbose_name = 'Prova'
        verbose_name_plural = 'Provas'

    def __unicode__(self):
        return self.titulo

class ProvaSobre(models.Model):
    assunto = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'

    def __unicode__(self):
        return self.assunto
            
class Questao(models.Model):
    TIPO = (
            (u'ME', u'Multipla Escolha'),
            (u'VF', u'Verdadeiro ou Falso'),
            (u'ES', u'Escolha Simples'),
        )

    questao = models.CharField(_('Questao'), max_length=300)
    sobre = models.ForeignKey('QuestaoSobre')
    tipo = models.CharField(max_length=2, choices=TIPO)
    dificuldade = models.ForeignKey('QuestaoDificuldade')   
    image = models.ImageField(_('Imagem'), upload_to='question/img')
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

    def __unicode__(self):
        return self.questao

class Resposta(models.Model):
    questao = models.ForeignKey(Questao)
    resposta = models.CharField(_('Resposta'), max_length=500)
    correta = models.BooleanField()
    alternativa = models.CharField(max_length=1)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    def __unicode__(self):
        return self.resposta
            
class QuestaoSobre(models.Model):
    sobre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Assunto'
        verbose_name_plural = 'Assuntos'

    def __unicode__(self):
        return self.sobre

class QuestaoDificuldade(models.Model):
    dificuldade = models.CharField(_('dificuldade'), max_length=10)
    peso = models.IntegerField(_('peso'))

    class Meta:
        verbose_name = 'Dificuldade'
        verbose_name_plural = 'Dificuldades'

    def __unicode__(self):
        return self.dificuldade
            
class UsuarioProva(models.Model):
    user = models.ForeignKey('core.Profile', blank=True, null=True)
    prova = models.ForeignKey(Prova)
    data_expiracao = models.DateTimeField()
    tempo_inicial = models.DateTimeField(blank=True, null=True)
    tempo_final = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Aplicar Prova'
        verbose_name_plural = 'Aplicar Provas'

    def __unicode__(self):
        return u"%s %s" %(self.user, self.prova)

    def has_finished(self):
        if self.tempo_inicial and self.tempo_final:
            return True
        else: 
            return False
        get_finished.boolean = True
        get_finished.short_description = 'Prova concluida?'

    def has_expired(self):
        return timezone.now() > self.data_expiracao
        get_expired.boolean = True
        get_expired.short_description = 'Tempo esgotado?'

    def get_questions(self):
        return self.prova.questoes.count()
        
    def get_progress(self):
        total_questoes = self.prova.questoes.count()
        questoes_respondidas = UsuarioProvaResposta.objects.filter(usuario_prova__id=self.id).count()
        current_progress = float(questoes_respondidas) / float(total_questoes) * 100
        current_progress = int(round(current_progress))
        return '{progress}%'.format(progress=current_progress)

    def get_score_for_pie(self):
        questoes = self.prova.questoes.count()
        respostas = self.usuarioprovaresposta_set.filter(resposta_alternativa__correta=True).count()
        score_exam = (float(respostas) / float(questoes)) * 100
        return int(round(score_exam))

    def get_score(self):
        questoes = self.prova.questoes.count()
        respostas = self.usuarioprovaresposta_set.filter(resposta_alternativa__correta=True).count()
        score_exam = (float(respostas) / float(questoes)) * 100
        score_exam = int(round(score_exam))
        return '{score}%'.format(score=score_exam)

    def get_title_exam(self):
        usuarios_lista = UsuarioProva.objects.filter(user__id=self.user.id)
        lista = []
        for user in usuarios_lista:
            lista.append(user.prova.titulo)
        return list(lista)

    def get_status(self):
        if self.has_finished():
            return 'Finalizada!'
        elif self.has_expired():
            return 'Expirou'
        elif self.tempo_inicial and not self.tempo_final:
            return 'Em Andamento'
        else:
            return 'Nova'
    get_status.short_description = 'Status'                 

class UsuarioProvaResposta(models.Model):
    usuario_prova = models.ForeignKey(UsuarioProva)
    questao = models.ForeignKey(Questao)
    resposta_alternativa = models.ForeignKey(Resposta)