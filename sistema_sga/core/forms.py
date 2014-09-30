# coding: utf-8
from django import forms
from django.contrib.auth.models import AbstractUser, User
from sistema_sga.core.models import Profile, Contact
from django.utils.translation import ugettext as _

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
                'picture', 'college','first_name', 'last_name','username','email', 'social_link_fc'
                )   

class SignupForm(forms.Form):
    college = forms.CharField(widget=forms.TextInput(
                              attrs={'class':'form-control','placeholder':'Universidade'}), 
                              max_length=100, label='Universidade ou Instituição de Ensino'
                            )

    def signup(self, request, user):
        user.college = self.cleaned_data['college']
        user.save()

class ContactForm(forms.ModelForm):
    business = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Empresa', 'required':'required'}), max_length=100)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nome', 'required':'required'}), max_length=100)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email', 'required':'required'}), max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Mensagem', 'rows': '4', 'required':'required'}), max_length=100)

    class Meta:
        model = Contact
        fields = ['business', 'name', 'email', 'message']