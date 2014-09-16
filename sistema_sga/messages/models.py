# coding: utf-8
from django.db import models

from sistema_sga.core.models import Profile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Max

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey('core.Profile', related_name='+')
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey('core.Profile', related_name='+')
    from_user = models.ForeignKey('core.Profile', related_name='+')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Mensagem')
        verbose_name_plural = _('Mensagens')
        ordering = ('date',)

    def __unicode__(self):
        return self.message

    @staticmethod
    def get_conversations(user):
        conversations = Message.objects.filter(user=user).values('conversation').annotate(last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user': Profile.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': Message.objects.filter(user=user, conversation__pk=conversation['conversation'], is_read=False).count(),
                })
        return users