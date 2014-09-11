# coding: utf-8
from django import forms
from django.contrib.auth.models import AbstractUser, User
from sistema_sga.core.models import Profile
from django.utils.translation import ugettext as _

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
					'first_name', 'last_name','username','email', 'social_link_fc'
				)	

class SignupForm(forms.Form):
    college = forms.CharField(max_length=100, label='Universidade ou Instituição de Ensino')

    def signup(self, request, user):
        user.college = self.cleaned_data['college']
        user.save()