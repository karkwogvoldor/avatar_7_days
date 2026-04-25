import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avatar_7_days.settings')
django.setup()

from avatar_app.models import Personagem
import re

FALSOS_POSITIVOS = {
    "professor", "general", "doctor", "animal", "capital", "normal",
    "natural", "original", "cultural", "central", "final", "local",
    "for", "of", "the", "and", "or", "in", "at", "by",
    "o", "a", "e", "de", "da", "do", "em", "no", "na",
    "source", "culture", "sun", "club", "fan", "official", "time",
    "avatar", "city", "republic",
}

def parece_ingles(texto):
    if not texto or texto in ["Nenhum", "—", ""]:
        return False

    palavras_ingles = [
        "man", "woman", "boy", "girl", "young", "former",
        "owner", "maker", "keeper", "hunter", "fighter", "rider",
        "trainer", "worker", "builder", "seller", "driver",
        "doorman", "wanderer", "outpost", "circus", "prison", "royal",
        "northern", "southern", "eastern", "western",
        "member", "agent", "officer",
        "crew", "group", "clan", "tribe", "nation", "kingdom",
        "town", "village", "island", "temple", "palace",
        "student", "teacher", "nurse",
        "merchant", "farmer", "fisherman", "blacksmith",
        " and ", " the ",
    ]

    texto_lower = texto.lower()

    if texto_lower.strip() in FALSOS_POSITIVOS:
        return False

    for palavra in palavras_ingles:
        if palavra in [" and ", " the "]:
            if palavra in texto_lower:
                return True
        else:
            # Só detecta palavras com mais de 4 letras que não são falsos positivos
            if len(palavra) > 4 and palavra not in FALSOS_POSITIVOS:
                if re.search(r'\b' + palavra + r'\b', texto_lower):
                    return True
    return False

nomes_ingles = set()
afiliacoes_ingles = set()
aliados_ingles = set()
inimigos_ingles = set()

for p in Personagem.objects.all():
    if parece_ingles(p.nome):
        nomes_ingles.add(p.nome)
    if parece_ingles(p.afiliacao):
        afiliacoes_ingles.add(p.afiliacao)
    for item in p.aliados.split(","):
        item = item.strip()
        if parece_ingles(item):
            aliados_ingles.add(item)
    for item in p.inimigos.split(","):
        item = item.strip()
        if parece_ingles(item):
            inimigos_ingles.add(item)

print("=" * 60)
print(f"NOMES em inglês ({len(nomes_ingles)}):")
for t in sorted(nomes_ingles): print(f"  - {t}")

print(f"\nAFILIAÇÕES em inglês ({len(afiliacoes_ingles)}):")
for t in sorted(afiliacoes_ingles): print(f"  - {t}")

print(f"\nALIADOS em inglês ({len(aliados_ingles)}):")
for t in sorted(aliados_ingles): print(f"  - {t}")

print(f"\nINIMIGOS em inglês ({len(inimigos_ingles)}):")
for t in sorted(inimigos_ingles): print(f"  - {t}")

total = len(nomes_ingles) + len(afiliacoes_ingles) + len(aliados_ingles) + len(inimigos_ingles)
print(f"\nTOTAL de termos únicos a corrigir: {total}")
print("=" * 60)