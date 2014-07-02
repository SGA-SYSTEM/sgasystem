# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

# import user
from django.contrib.auth.models import User

class Prova(models.Model):
	titulo = models.CharField(_('titulo'), max_length=200, blank=True, null=False)
	created_at = models.DateTimeField(_('criado em'), auto_now_add=True, auto_now=False)
	sobre = models.ForeignKey('ProvaSobre')
	questoes = models.ManyToManyField('Questao', verbose_name=_('Questões'))
	duracao = models.IntegerField(_('Período'))

	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = 'Prova'
		verbose_name_plural = 'Provas'

class ProvaSobre(models.Model):
	assunto = models.CharField(max_length=50)

	def __unicode__(self):
		return self.assunto
	
	class Meta:
		verbose_name = 'Tópico'
		verbose_name_plural = 'Tópicos'
			
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

	def __unicode__(self):
		return self.questao

class Resposta(models.Model):
	questao = models.ForeignKey(Questao)
	resposta = models.CharField(_('Resposta'), max_length=500)
	correta = models.BooleanField()
	alternativa = models.CharField(max_length=1)

	def __unicode__(self):
		return self.resposta

	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'

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
	dificuldade = models.CharField(_('dificuldade'), max_length=10)
	peso = models.IntegerField(_('peso'))

	def __unicode__(self):
		return self.dificuldade

	class Meta:
		verbose_name = 'Dificuldade'
		verbose_name_plural = 'Dificuldades'
			
class UsuarioProva(models.Model):
	user = models.ForeignKey(User)
	prova = models.ForeignKey(Prova)
	data_expiracao = models.DateTimeField()
	tempo_inicial = models.DateTimeField(blank=True, null=True)
	tempo_final = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u"%s %s" %(self.user, self.prova)

	def get_finished(self):
		if tempo_inicial and tempo_final:
			return True
		else: return False
	get_finished.boolean = True
	get_finished.short_description = 'Prova concluida?'

	def get_expired(self):
		return timezone.now() > self.tempo_final
	get_expired.boolean = True
	get_expired.short_description = 'Tempo esgotado?'

	def get_progress(self):
		total_questoes = self.prova.questoes.count()
		questoes_respondidas = UsuarioProvaResposta.objects.filter(usuario_prova_id=self.id).count()
		current_progress = float(questoes_respondidas) / float(total_questoes) * 100

	def get_status(self):
		if self.has_finished():
			return 'Finalizada!'
		elif self.has_expired():
			return 'Expirou ;('
		elif self.start_time and not self.end_time:
			return 'Em Andamento'
		else:
			return 'Nova'
	get_status.short_description = 'Status'					

	class Meta:
		verbose_name = 'Aplicar Prova'
		verbose_name_plural = 'Aplicar Provas'

class UsuarioProvaResposta(models.Model):
	usuario_prova = models.ForeignKey(UsuarioProva)
	questao = models.ForeignKey(Questao)
	resposta_alternativa = models.ForeignKey(Resposta)