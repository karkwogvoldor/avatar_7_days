from django.db import models

# Create your models here.

from django.db import models

class Personagem(models.Model):
    nome = models.CharField(max_length=100)
    afiliacao = models.CharField(max_length=100)
    aliados = models.TextField(default="Nenhum")
    inimigos = models.TextField()
    foto_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.nome