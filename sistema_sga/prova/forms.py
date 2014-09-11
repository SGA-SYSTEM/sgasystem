
from django import forms
from sistema_sga.prova.models import *

class ProvaForm(forms.ModelForm):
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=255)
    sobre = forms.ChoiceField(choices=(), widget=forms.Select(attrs={'class':'form=control'}))


    def __init__(self, *args, **kwargs):
        super(ProvaForm, self).__init__(*args, **kwargs)
        choices = [(x.id, unicode(x)) for x in ProvaSobre.objects.all()]
        self.fields['sobre'].choices = choices

    class Meta:
        model = Prova
        fields = ['titulo', 'sobre']

class QuestaoForm(forms.ModelForm):
    questoes = forms.ChoiceField(choices=(), widget=forms.Select(attrs={'multiple':'multiple', 'class':'form-control'}), help_text='Mantenha o "Control", ou "Command" no Mac, pressionado para selecionar mais de uma opcao.')
    duracao = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(QuestaoForm, self).__init__(*args, **kwargs)
        choices = [(x.id, unicode(x)) for x in Questao.objects.all()]
        self.fields['questoes'].choices = choices

    class Meta:
        model = Questao
        fields = ['questoes', 'duracao']