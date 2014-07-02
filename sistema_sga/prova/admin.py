# coding: utf-8

from django.contrib import admin

from sistema_sga.prova.models import Prova, Questao, Resposta

from django.utils.timezone import now

from django.utils.translation import ungettext, ugettext as _

# Register your models here.

class RespostaInline(admin.TabularInline):
		model = Resposta
		fields = ['alternativa', 'resposta', 'correta']
		extra = 3

class ProvaAdmin(admin.ModelAdmin):
			list_display = ('titulo','questoes','duracao','created_at')
			date_hierarchy = 'created_at' # install pytz --> pip install pytz
			search_fields = ('titulo', 'created_at')
			list_filter = ['created_at']

class QuestaoAdmin(admin.ModelAdmin):
		list_display = ['questao', 'sobre', 'tipo', 'dificuldade', 'ativo', 'image']
		list_display = ['tipo', 'dificuldade', 'ativo']
		inlines = [RespostaInline]				
		
admin.site.register(Prova, ProvaAdmin)
admin.site.register(Questao, QuestaoAdmin)