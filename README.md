🌊 Avatar: The Last Airbender — Tradutor & Lore
Uma aplicação interativa focada no universo de Avatar, que oferece consultas ao Lore em dois idiomas, mecanismo de busca avançado e tradução temática.

🔗 Deploy Oficial
Acesse o projeto online:

https://avatar7days-production.up.railway.app/

🧩 Componentes
avatar_7_days/
│
├── setup/                # Configurações principais do projeto Django
│   ├── settings.py       # Configurações gerais e DB
│   ├── urls.py           # Rotas globais do projeto
│   └── wsgi.py           # Interface de servidor para Gunicorn
│
├── galeria/              # App principal (Lore e Personagens)
│   ├── static/           # CSS, JS e Imagens das Nações
│   ├── templates/        # Arquivos HTML (index, busca, tradutor)
│   ├── models.py         # Modelos com suporte a dois idiomas
│   ├── views.py          # Lógica de busca e filtragem
│   └── urls.py           # Rotas específicas do app
│
├── manage.py             # CLI do Django
├── Procfile              # Configuração de execução no Railway (Gunicorn)
├── requirements.txt      # Dependências (Django, Gunicorn, Psycopg2)
└── runtime.txt           # Versão do Python para o deploy
⚙️ Funcionalidades Principais
1. Conteúdo Bilíngue (PT-BR & Original)
Todas as informações do Lore e descrições de personagens estão disponíveis em Português (PT-BR) e na Língua Original para consulta e comparação técnica.

2. Mecanismo de Busca
Barra de pesquisa integrada que permite localizar personagens, termos de dobra ou eventos históricos filtrando diretamente no banco de dados PostgreSQL.

3. Infraestrutura de Produção
Servidor: Utiliza o Gunicorn (Green Unicorn) para gerenciar as requisições de forma robusta e escalável.

Deploy: Configurado para entrega contínua através do Railway, garantindo alta disponibilidade do serviço.  

🚀 Setup Local
1. Clone o repositório
Bash
git clone https://github.com/karkwogvoldor/avatar_7_days.git
cd avatar_7_days
2. Configuração do Ambiente
Bash
python -m venv venv
# Ativar venv (Windows: venv\Scripts\activate | Linux: source venv/bin/activate)
pip install -r requirements.txt
3. Execução com Gunicorn (Simulação de Produção)
Bash
gunicorn setup.wsgi
📄 Licença
Este projeto está licenciado sob a MIT License.
