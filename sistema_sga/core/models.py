# coding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, User

from cloudinary.models import CloudinaryField


# Create your models here.
class Profile(AbstractUser):
    social_link_fc = models.CharField(_(u'Facebook'), max_length=200,
                                      blank=True, null=True)
    college = models.CharField(_(u'Instituição de Ensino'), max_length=200,
                               blank=True, null=True)

    picture = CloudinaryField(_(u'foto'), blank=True, null=True)

    def __unicode__(self):
        return u'{username} - ({email})'.format(username=self.username,
                                                email=self.email)

    def get_screen_name(self):
        try:
            if self.get_full_name():
                return self.get_full_name()
            else:
                return self.username
        except:
            return self.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class Contact(models.Model):
    business = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField(max_length=500, verbose_name='Mensagem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Mensagem para " + str(self.email)
