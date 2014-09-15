# coding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import AbstractUser, User

# Create your models here.

from django.contrib.auth.models import AbstractUser, User
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin

class Profile(AbstractUser):
    social_link_fc = models.CharField(_(u'Facebook'), max_length=200,
                                     blank=True, null=True)
    # college = models.CharField(_(u'Universidade ou Instituição de Ensino'), max_length=200,
                                     # blank=True, null=True)

    def __unicode__(self):
        return u'{username} - ({email})'.format(username=self.username,
                                              email=self.email)