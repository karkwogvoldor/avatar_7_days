import os
import django
import requests
import re
from constants import NACOES, CARGOS, NOMES_BLOQUEADOS, DICIONARIO_AVATAR, LUGARES_AVATAR, PARENTESCO_AVATAR

# --- CONFIGURAÇÃO DJANGO ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avatar_7_days.settings')
django.setup()
from avatar_app.models import Personagem


# ---------------------------------------------------------------------------
# TODOS OS DICIONÁRIOS UNIDOS — ordem de prioridade
# ---------------------------------------------------------------------------
TODOS_OS_TERMOS: dict = {
    **DICIONARIO_AVATAR,
    **NACOES,
    **LUGARES_AVATAR,
    **CARGOS,
    **PARENTESCO_AVATAR,
}


# ---------------------------------------------------------------------------
# TRADUÇÃO OFFLINE
# ---------------------------------------------------------------------------

def eh_nome_proprio(termo: str) -> bool:
    """Verifica se o termo é um nome próprio bloqueado."""
    termo_limpo = termo.strip()
    for nome in NOMES_BLOQUEADOS:
        if nome.lower() == termo_limpo.lower():
            return True
    return False


def traduzir_termo(termo: str) -> str:
    """
    Tenta traduzir um termo usando os dicionários locais.
    Prioridade:
    1. Match exato no dicionário completo
    2. Nome próprio bloqueado → retorna como está
    3. Match parcial — substitui subtextos conhecidos dentro do termo
    4. Sem tradução → retorna original
    """
    if not termo or not termo.strip():
        return ""

    termo = termo.strip()

    # 1. Match exato
    if termo in TODOS_OS_TERMOS:
        return TODOS_OS_TERMOS[termo]

    # 2. Nome próprio — não traduz
    if eh_nome_proprio(termo):
        return termo

    # 3. Match parcial — substitui partes conhecidas dentro do texto
    resultado = termo
    for en, pt in sorted(TODOS_OS_TERMOS.items(), key=lambda x: len(x[0]), reverse=True):
        if en.lower() in resultado.lower():
            resultado = re.sub(re.escape(en), pt, resultado, flags=re.IGNORECASE)

    if resultado != termo:
        return resultado.strip()

    # 4. Sem tradução — retorna o original
    return termo


def traduzir_lista(lista: list) -> str:
    """Traduz uma lista de aliados/inimigos e retorna string limpa."""
    itens = [i.strip() for i in lista if i and i.strip()]
    if not itens:
        return "Nenhum"
    traduzidos = [traduzir_termo(i) for i in itens]
    return ", ".join(traduzidos)


def separar_afiliacoes_coladas(texto_raw: str) -> str:
    """
    Separa afiliações grudadas em texto corrido buscando termos conhecidos.
    """
    if not texto_raw:
        return ""

    termos_busca = (
        list(NACOES.keys()) +
        list(CARGOS.keys()) +
        list(DICIONARIO_AVATAR.keys()) +
        list(LUGARES_AVATAR.keys()) +
        ["military", "army", "navy", "police", "forces"]
    )

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


def limpar_lista(lista: list) -> list:
    """Remove itens vazios e espaços extras."""
    return [i.strip() for i in lista if i and i.strip()]


# ---------------------------------------------------------------------------
# IMPORTAÇÃO PRINCIPAL
# ---------------------------------------------------------------------------

def importar_e_traduzir():
    api_url = 'https://last-airbender-api.fly.dev/api/v1/characters?perPage=1000'

    try:
        print("Buscando dados da API Avatar...")
        response = requests.get(api_url)
        lista_personagens = response.json()
        print(f"Total de personagens encontrados: {len(lista_personagens)}")

        for p in lista_personagens:

            # 1. NOME
            nome_original = p.get('name', '') or ''
            if eh_nome_proprio(nome_original.strip()):
                nome_pt = nome_original.strip()
            else:
                nome_pt = traduzir_termo(nome_original) or "Sem nome"

            # 2. AFILIAÇÃO
            afiliacao_raw = p.get('affiliation') or ""
            if afiliacao_raw.strip() in TODOS_OS_TERMOS:
                afiliacao_pt = TODOS_OS_TERMOS[afiliacao_raw.strip()]
            else:
                afiliacao_separada = separar_afiliacoes_coladas(afiliacao_raw)
                afiliacao_pt = traduzir_termo(afiliacao_separada)

            # 3. ALIADOS E INIMIGOS
            aliados_pt = traduzir_lista(p.get('allies', []))
            inimigos_pt = traduzir_lista(p.get('enemies', []))

            # 4. FOTO
            foto_url_original = p.get('photoUrl')
            foto_url_final = (
                ""
                if not foto_url_original or foto_url_original == "None"
                else foto_url_original
            )

            # 5. SALVA NO BANCO
            personagem, created = Personagem.objects.update_or_create(
                nome=nome_pt,
                defaults={
                    'afiliacao': afiliacao_pt,
                    'aliados': aliados_pt,
                    'inimigos': inimigos_pt,
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