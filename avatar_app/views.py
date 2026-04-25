from django.shortcuts import render
from django.db.models import Case, When, Value, IntegerField
from .models import Personagem

PERSONAGENS_PRINCIPAIS = [
    # Avatar: A Lenda de Aang
    "Aang", "Katara", "Sokka", "Toph", "Zuko", "Iroh", "Azula",
    "Appa", "Momo", "Suki", "Ozai", "Pakku", "Bumi", "Jet",
    "Mai", "Ty Lee", "Ursa", "Hakoda", "Yue", "Roku", "Toph Beifong", "Bumi (Rei de Omashu)",

    # Avatar: A Lenda de Korra
    "Korra", "Mako", "Bolin", "Asami", "Tenzin", "Lin",
    "Amon", "Zaheer", "Kuvira", "Tarrlok", "Unalaq",
    "Jinora", "Ikki", "Meelo", "Varrick", "Zhu Li",
    "Suyin", "Opal", "Desna", "Eska",
]

def home(request):
    # Busca os nomes traduzidos dos personagens principais no banco
    nomes_principais = list(
        Personagem.objects.filter(nome_en__in=PERSONAGENS_PRINCIPAIS)
        .values_list('nome', flat=True)
    )

    personagens = Personagem.objects.annotate(
        prioridade=Case(
            *[When(nome=nome, then=Value(0)) for nome in nomes_principais],
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('prioridade', 'nome')

    return render(request, 'avatar_app/home.html', {
        'personagens': personagens,
        'total_principais': len(nomes_principais),
    })