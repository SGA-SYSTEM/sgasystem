# coding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, User

from django.conf import settings

import os.path

# Create your models here.

from django.contrib.auth.models import AbstractUser, User
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin

class Profile(AbstractUser):
    social_link_fc = models.CharField(_(u'Facebook'), max_length=200,
                                     blank=True, null=True)
    college = models.CharField(_(u'Instituição de Ensino'), max_length=200,
                                     blank=True, null=True)

    def __unicode__(self):
        return u'{username} - ({email})'.format(username=self.username,
                                              email=self.email)

def create_user_profile(sender, instance, created, **kwargs):
 	if created:
    	Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)