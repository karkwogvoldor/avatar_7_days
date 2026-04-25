from django.db import models

class Personagem(models.Model):
    # Campos em português
    nome = models.CharField(max_length=200)
    afiliacao = models.CharField(max_length=500, blank=True, default="")
    aliados = models.TextField(default="Nenhum")
    inimigos = models.TextField(default="Nenhum")
    foto_url = models.URLField(max_length=500, null=True, blank=True)

    # Campos originais em inglês
    nome_en = models.CharField(max_length=200, default="")
    afiliacao_en = models.CharField(max_length=500, blank=True, default="")
    aliados_en = models.TextField(default="")
    inimigos_en = models.TextField(default="")

    def __str__(self):
        return self.nome