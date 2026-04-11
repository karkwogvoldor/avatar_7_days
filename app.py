import json
import requests
from googletrans import Translator
import sys

# Garante que o terminal aceite acentos
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def personagens():
    translator = Translator()
    api_url = 'https://last-airbender-api.fly.dev/api/v1/characters'
    
    try:
        response = requests.get(api_url)
        lista_personagens = response.json()
        
        # Traduzindo apenas os 3 primeiros para teste (evita bloqueio de IP)
        for p in lista_personagens[:3]:
            for chave in ['enemies', 'affiliation']:
                if chave in p and p[chave]:
                    # Tradução direta
                    res = translator.translate(str(p[chave]), dest='pt')
                    p[chave] = res.text
        
        # O segredo do acento no print está no ensure_ascii=False
        print(json.dumps(lista_personagens[:3], indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Erro: {e}")

personagens()