import os
import django
import requests
import re
from constants import NACOES, CARGOS, NOMES_BLOQUEADOS, DICIONARIO_AVATAR, LUGARES_AVATAR, PARENTESCO_AVATAR, PRIORIDADE_ALTA

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avatar_7_days.settings')
django.setup()
from avatar_app.models import Personagem

TODOS_OS_TERMOS: dict = {
    **PRIORIDADE_ALTA,
    **DICIONARIO_AVATAR,
    **NACOES,
    **LUGARES_AVATAR,
    **CARGOS,
    **PARENTESCO_AVATAR,
}

def eh_nome_proprio(termo):
    for nome in NOMES_BLOQUEADOS:
        if nome.lower() == termo.strip().lower():
            return True
    return False

def traduzir_termo(termo):
    if not termo or not termo.strip():
        return ""
    termo = termo.strip()
    if termo in TODOS_OS_TERMOS:
        return TODOS_OS_TERMOS[termo]
    if eh_nome_proprio(termo):
        return termo
    resultado = termo
    for en, pt in sorted(TODOS_OS_TERMOS.items(), key=lambda x: len(x[0]), reverse=True):
        if en.lower() in resultado.lower():
            resultado = re.sub(re.escape(en), pt, resultado, flags=re.IGNORECASE)
    conectivos = [(" and ", " e "), (" or ", " ou ")]
    for en, pt in conectivos:
        resultado = resultado.replace(en, pt)
    if resultado != termo:
        return resultado.strip()
    return termo

def traduzir_lista(lista):
    itens = [i.strip() for i in lista if i and i.strip()]
    if not itens:
        return "Nenhum"
    return ", ".join(traduzir_termo(i) for i in itens)

def lista_para_str(lista):
    itens = [i.strip() for i in lista if i and i.strip()]
    return ", ".join(itens) if itens else "Nenhum"

def separar_afiliacoes_coladas(texto_raw):
    if not texto_raw:
        return ""
    TERMOS_IGNORADOS = {"for","of","the","and","or","in","at","by","with","General","Master","Officer","Guard","Leader","Monk"}
    termos_busca = list(NACOES.keys()) + list(DICIONARIO_AVATAR.keys()) + list(LUGARES_AVATAR.keys())
    termos_busca = [t for t in termos_busca if len(t) >= 5 and t not in TERMOS_IGNORADOS]
    encontrados = []
    for termo in termos_busca:
        if termo.lower() in texto_raw.lower() and termo not in encontrados:
            encontrados.append(termo)
    if not encontrados:
        return texto_raw
    encontrados_limpos = []
    for e in sorted(encontrados, key=len, reverse=True):
        if not any(e.lower() in outro.lower() for outro in encontrados_limpos if e != outro):
            encontrados_limpos.append(e)
    return ", ".join(encontrados_limpos)

def importar_e_traduzir():
    api_url = 'https://last-airbender-api.fly.dev/api/v1/characters?perPage=1000'
    try:
        print("Buscando dados da API Avatar...")
        response = requests.get(api_url)
        lista_personagens = response.json()
        print(f"Total: {len(lista_personagens)} personagens")

        for p in lista_personagens:
            nome_original = p.get('name', '') or ''
            afiliacao_original = p.get('affiliation') or ''
            aliados_original = p.get('allies', [])
            inimigos_original = p.get('enemies', [])

            # Português
            nome_pt = (nome_original if eh_nome_proprio(nome_original.strip()) else traduzir_termo(nome_original)) or "Sem nome"
            if afiliacao_original.strip() in TODOS_OS_TERMOS:
                afiliacao_pt = TODOS_OS_TERMOS[afiliacao_original.strip()]
            else:
                afiliacao_pt = traduzir_termo(separar_afiliacoes_coladas(afiliacao_original))
            aliados_pt = traduzir_lista(aliados_original)
            inimigos_pt = traduzir_lista(inimigos_original)

            # Inglês original
            nome_en = nome_original.strip()
            afiliacao_en = afiliacao_original.strip()
            aliados_en = lista_para_str(aliados_original)
            inimigos_en = lista_para_str(inimigos_original)

            foto_url_original = p.get('photoUrl')
            foto_url_final = "" if not foto_url_original or foto_url_original == "None" else foto_url_original

            personagem, created = Personagem.objects.update_or_create(
                nome_en=nome_en,
                defaults={
                    'nome': nome_pt,
                    'afiliacao': afiliacao_pt,
                    'aliados': aliados_pt,
                    'inimigos': inimigos_pt,
                    'afiliacao_en': afiliacao_en,
                    'aliados_en': aliados_en,
                    'inimigos_en': inimigos_en,
                    'foto_url': foto_url_final,
                }
            )
            status = "Criado" if created else "Atualizado"
            print(f"  [{status}] {nome_pt}")

        print("\nImportação concluída com sucesso!")
    except Exception as e:
        print(f"Erro geral: {e}")
        raise

if __name__ == '__main__':
    importar_e_traduzir()