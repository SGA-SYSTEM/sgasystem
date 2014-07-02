# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Prova'
        db.create_table(u'prova_prova', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('questoes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.Questao'])),
            ('duracao', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'prova', ['Prova'])

        # Adding model 'Questao'
        db.create_table(u'prova_questao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questao', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('sobre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.QuestaoSobre'])),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('dificuldade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.QuestaoDificuldade'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('ativo', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'prova', ['Questao'])

        # Adding model 'QuestaoSobre'
        db.create_table(u'prova_questaosobre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sobre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'prova', ['QuestaoSobre'])

        # Adding model 'QuestaoDificuldade'
        db.create_table(u'prova_questaodificuldade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dificuldade', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('peso', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'prova', ['QuestaoDificuldade'])

        # Adding model 'Resposta'
        db.create_table(u'prova_resposta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resposta', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('correta', self.gf('django.db.models.fields.BooleanField')()),
            ('alternativa', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'prova', ['Resposta'])

        # Adding model 'UsuarioProva'
        db.create_table(u'prova_usuarioprova', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('prova', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.Prova'])),
            ('data_expiracao', self.gf('django.db.models.fields.DateTimeField')()),
            ('tempo_inicial', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('tempo_final', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'prova', ['UsuarioProva'])

        # Adding model 'UsuarioProvaResposta'
        db.create_table(u'prova_usuarioprovaresposta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario_prova', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.UsuarioProva'])),
            ('questao', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.Questao'])),
            ('resposta_alternativa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prova.Resposta'])),
        ))
        db.send_create_signal(u'prova', ['UsuarioProvaResposta'])


    def backwards(self, orm):
        # Deleting model 'Prova'
        db.delete_table(u'prova_prova')

        # Deleting model 'Questao'
        db.delete_table(u'prova_questao')

        # Deleting model 'QuestaoSobre'
        db.delete_table(u'prova_questaosobre')

        # Deleting model 'QuestaoDificuldade'
        db.delete_table(u'prova_questaodificuldade')

        # Deleting model 'Resposta'
        db.delete_table(u'prova_resposta')

        # Deleting model 'UsuarioProva'
        db.delete_table(u'prova_usuarioprova')

        # Deleting model 'UsuarioProvaResposta'
        db.delete_table(u'prova_usuarioprovaresposta')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'prova.prova': {
            'Meta': {'object_name': 'Prova'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duracao': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questoes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.Questao']"}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'prova.questao': {
            'Meta': {'object_name': 'Questao'},
            'ativo': ('django.db.models.fields.BooleanField', [], {}),
            'dificuldade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.QuestaoDificuldade']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'questao': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'sobre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.QuestaoSobre']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'prova.questaodificuldade': {
            'Meta': {'object_name': 'QuestaoDificuldade'},
            'dificuldade': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.IntegerField', [], {})
        },
        u'prova.questaosobre': {
            'Meta': {'object_name': 'QuestaoSobre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sobre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'prova.resposta': {
            'Meta': {'object_name': 'Resposta'},
            'alternativa': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'correta': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resposta': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'prova.usuarioprova': {
            'Meta': {'object_name': 'UsuarioProva'},
            'data_expiracao': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prova': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.Prova']"}),
            'tempo_final': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tempo_inicial': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'prova.usuarioprovaresposta': {
            'Meta': {'object_name': 'UsuarioProvaResposta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.Questao']"}),
            'resposta_alternativa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.Resposta']"}),
            'usuario_prova': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prova.UsuarioProva']"})
        }
    }

    complete_apps = ['prova']