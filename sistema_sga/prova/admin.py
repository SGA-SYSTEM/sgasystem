# coding: utf-8

from django.contrib import admin

from sistema_sga.prova.models import Prova, Questao, Resposta, QuestaoSobre, ProvaSobre, QuestaoDificuldade, UsuarioProva

from django.utils.timezone import now

from django.utils.translation import ungettext, ugettext as _

# Register your models here.

class RespostaInline(admin.TabularInline):
        model = Resposta
        fields = ['alternativa', 'resposta', 'correta']
        extra = 1

class ProvaAdmin(admin.ModelAdmin):
            list_display = ('titulo','duracao','created_at')
            date_hierarchy = 'created_at' # install pytz --> pip install pytz
            search_fields = ('titulo', 'created_at')
            list_filter = ['created_at']
        

class QuestaoAdmin(admin.ModelAdmin):
        list_display = ['questao', 'sobre', 'tipo', 'dificuldade', 'ativo', 'image']
        list_display = ['questao','tipo', 'dificuldade', 'ativo']
        inlines = [RespostaInline]             

class UsuarioProvaAdmin(admin.ModelAdmin):
      fields = ['user', 'prova', 'data_expiracao']
      list_display = ['id', 'user', 'prova', 'data_expiracao', 'get_status', 'has_finished', 'has_expired']
      date_hierarchy = 'data_expiracao'
      search_fields = ['user__username', 'user__first_name', 'user__last_name', 'prova__name']
      list_filter = ['data_expiracao']
          
        
admin.site.register(Prova, ProvaAdmin)
admin.site.register(ProvaSobre)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(QuestaoSobre)
admin.site.register(QuestaoDificuldade)
admin.site.register(UsuarioProva, UsuarioProvaAdmin)