from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Personagem

def home(request):
    # Busca todos os personagens cadastrados no banco de dados
    personagens = Personagem.objects.all()
    
    # Envia a lista para o arquivo HTML
    return render(request, 'avatar_app/home.html', {'personagens': personagens})