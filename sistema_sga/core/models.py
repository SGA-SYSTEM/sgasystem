#coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Prova(models.Model):
	titulo = models.CharField(_('titulo')max_length=200, blank=True, null=False)
	created_at = models.DateTimeField(_('criado em')auto_now_add=True, auto_now=False)
	questoes = models.ForeignKey('Questao', verbose_name=_('Questões'))
	duracao = models.IntegerField()

	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = 'Prova'
		verbose_name_plural = 'Provas'
			
class Questao(models.Model):
	TIPO = (
			(u'ME', u'Multipla Escolha'),
			(u'VF', u'Verdadeiro ou Falso'),
			(u'ES', u'Escolha Simples'),
		)
	questao = models.CharField()
	sobre = models.ForeignKey('QuestaoSobre')
	tipo = models.CharField(max_length=2, choices=TIPO)
	dificuldade = models.ForeignKey('QuestaoDificuldade')	
	image = models.ImageField(blank=True, null=True)
	ativo = models.BooleanField()

	def __unicode__(self):
		return self.questao

	class Meta:
		verbose_name = 'Questão'
		verbose_name_plural = 'Questões'
			
class QuestaoSobre(models.Model):
	sobre = models.CharField(max_length=100)

	def __unicode__(self):
		return self.sobre

	class Meta:
		verbose_name = 'Assunto'
		verbose_name_plural = 'Assuntos'
			
class QuestaoDificuldade(models.Model):
	dificuldade = models.CharField(max_length=10)
	peso = models.IntegerField(max_digits=1)

	def __unicode__(self):
		return self.dificuldade

	class Meta:
		verbose_name = 'Dificuldade'
		verbose_name_plural = 'Dificuldades'
			
class Resposta(models.Model):
	resposta = models.CharField(max_length=10)
	correta = models.BooleanField()
	alternativa = models.CharField(max_length=1)

	def __unicode__(self):
		return self.resposta

	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'
			
class UsuarioProva(models.Model):
	user = models.ForeignKey(User)
	prova = models.ForeignKey(Prova)
	data_expiracao = models.DateTimeField()
	tempo_inicial = models.DateTimeField(blank=True, null=True)
	tempo_final = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u"%s %s" %(self.user, self.prova)

	def finalizada(self):
		if tempo_inicial and tempo_final:
			return True
		else: return False
	finalizada.boolean = True
	finaliliza.short_description = 'Prova concluida?'

class UsuarioProvaResposta(models.Models):
	usuario_prova = models.ForeignKey(UsuarioProva)
	questao = models.ForeignKey(Questao)
	resposta_alternativa = models.ForeignKey(Resposta)