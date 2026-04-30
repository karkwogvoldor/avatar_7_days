# 🌊⚡ Avatar: The Last Airbender — Tradutor & Lore

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

Uma aplicação interativa focada no universo de Avatar, que oferece consultas ao Lore em dois idiomas, mecanismo de busca avançado e tradução temática.

## 🔗 Deploy Oficial
Acesse o projeto online:  
[https://avatar7days-production.up.railway.app/](https://avatar7days-production.up.railway.app/)

---

### 📸 Prévia

| Personagens Principais | Personagens Secundários |
|---|---|
| ![Principal](https://imgur.com/Ar7d9BI.png) | ![Secundário](https://imgur.com/5ciYqT3.png) |
| ![Azula](https://imgur.com/biooaAt.png) | ![Zuko](https://imgur.com/flzMdDG.png) |

> Personagens com fotos aparecem primeiro. Alterne entre 🇧🇷 Português e 🇺🇸 Inglês a qualquer momento.

---

## 🧩 Componentes

```text
avatar_7_days/
│
├── setup/               # Configurações principais do projeto Django
│   ├── settings.py      # Configurações gerais e DB
│   ├── urls.py          # Rotas globais do projeto
│   └── wsgi.py          # Interface de servidor para Gunicorn
│
├── galeria/             # App principal (Lore e Personagens)
│   ├── static/          # CSS, JS e Imagens das Nações
│   ├── templates/       # Arquivos HTML (index, busca, tradutor)
│   ├── models.py        # Modelos com suporte a dois idiomas
│   ├── views.py         # Lógica de busca e filtragem
│   └── urls.py          # Rotas específicas do app
│
├── manage.py            # CLI do Django
├── Procfile             # Configuração de execução no Railway (Gunicorn)
├── requirements.txt     # Dependências (Django, Gunicorn, Psycopg2)
└── runtime.txt          # Versão do Python para o deploy
```

## ⚙️ Funcionalidades Principais

### 🌐 Conteúdo Bilíngue (PT-BR & Original)
Todas as informações do Lore e descrições de personagens estão disponíveis em Português (PT-BR) e na Língua Original para consulta e comparação técnica.

### 🔎 Mecanismo de Busca
Barra de pesquisa integrada que permite localizar personagens, termos de dobra ou eventos históricos filtrando diretamente no banco de dados PostgreSQL.

### 🏗️ Infraestrutura de Produção
- **Servidor:** Utiliza o Gunicorn (Green Unicorn) para gerenciar as requisições de forma robusta e escalável.  
- **Deploy:** Configurado para entrega contínua através do Railway, garantindo alta disponibilidade do serviço.

---

## 🚀 Setup Local

### Clone o repositório
```bash
git clone https://github.com/karkwogvoldor/avatar_7_days.git
cd avatar_7_days
```

## ⚙️ Configuração do Ambiente

```bash
python -m venv venv
```

# Ativar venv:
```bash
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate
```

pip install -r requirements.txt

## 🚀 Execução com Gunicorn (Simulação de Produção)

```bash
gunicorn setup.wsgi
```

## 📄 Licença

Este projeto está licenciado sob a MIT License.
