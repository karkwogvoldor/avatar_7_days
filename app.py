import os
import django
import json
import requests
import time # <-- Adicionado para a pausa
from googletrans import Translator

# --- CONFIGURAÇÃO PARA O DJANGO RECONHECER O SCRIPT ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avatar_7_days.settings')
django.setup()
from avatar_app.models import Personagem 
# -----------------------------------------------------

def importar_e_traduzir():
    translator = Translator()
    api_url = 'https://last-airbender-api.fly.dev/api/v1/characters?perPage=1000'
    
    try:
        response = requests.get(api_url)
        lista_personagens = response.json()
        
        for p in lista_personagens:
            # 1. TRATANDO O NOME
            nome_original = p.get('name', 'Sem nome')
            
            # Palavras que indicam que o nome deve permanecer original
            palavras_bloqueadas = ['and', 'ping', 'poi', 'momo', 'appa', 'the']
            
            # Verifica se alguma palavra bloqueada está no nome
            contem_bloqueada = any(word.lower() in nome_original.lower() for word in palavras_bloqueadas)

            # Só traduz se tiver mais de 2 palavras E NÃO contiver palavras bloqueadas
            if len(nome_original.split()) > 2 and not contem_bloqueada:
                try:
                    nome_pt = translator.translate(nome_original, dest='pt').text
                except:
                    nome_pt = nome_original 
            else:
                nome_pt = nome_original

            # 2. TRATANDO A AFILIAÇÃO (Com proteção)
            afiliacao_original = p.get('affiliation') or 'Nenhum' # O "or" garante que vazios virem "Nenhum"
            try:
                afiliacao_pt = translator.translate(afiliacao_original, dest='pt').text
            except:
                afiliacao_pt = afiliacao_original

            # 3. TRATANDO OS INIMIGOS (Com proteção)
            inimigos_original = ", ".join(p.get('enemies', []))
            inimigos_pt = inimigos_original
            if inimigos_original:
                try:
                    inimigos_pt = translator.translate(inimigos_original, dest='pt').text
                except:
                    pass # Se falhar, continua com o original
            
            # 4. TRATANDO OS ALIADOS (Adicione isto)
            # Transforma a lista ['Aang', 'Appa'] em texto "Aang, Appa"
            aliados_texto = ", ".join(p.get('allies', []))

            # SALVANDO NO BANCO DO DJANGO
            Personagem.objects.get_or_create(
                nome=nome_pt,
                afiliacao=afiliacao_pt,
                aliados=aliados_texto or "Nenhum",
                inimigos=inimigos_pt or "Nenhum"
            )
            print(f"Salvo: {nome_pt}")
            
            # Pausa de meio segundo para o Google não bloquear você
            time.sleep(0.5)

    except Exception as e:
        print(f"Erro geral: {e}")

if __name__ == '__main__':
    importar_e_traduzir()