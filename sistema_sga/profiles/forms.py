# coding: utf-8
from django import forms
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import ugettext as _

class ProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
					'first_name', 'last_name','username','email'
				)	