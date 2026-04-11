from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Personagem # Importa o seu modelo

admin.site.register(Personagem)