from django.shortcuts import render
from sistema_sga.prova.models import Prova

# Create your views here.

def prova(request):
	provas = Prova.objects.all()
	context = ({'provas':provas},)
	return render(request, 'prova/provas.html', context)