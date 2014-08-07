# coding: utf-8
from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user)