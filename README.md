# ⚡ Avatar 7 Days

> A Django-powered encyclopedia of Avatar: The Last Airbender and The Legend of Korra characters — with bilingual support, smart offline translation, and a clean web interface.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📸 Preview

| Main Characters | Secondary Characters |
|---|---|
| ![Main](https://imgur.com/Ar7d9BI.png) | ![Secondary](https://imgur.com/5ciYqT3.png) |
| ![Azula](https://imgur.com/biooaAt.png) | ![Zuko](https://imgur.com/flzMdDG.png) |

> Characters with photos appear first. Toggle between 🇧🇷 Portuguese and 🇺🇸 English at any time.

---

## 🗂 Components

```
avatar_7_days/
│
├── avatar_7_days/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── avatar_app/             # Main application
│   ├── models.py           # Personagem model (PT + EN fields)
│   ├── views.py            # Home view with priority ordering
│   ├── urls.py             # URL routing
│   └── templates/
│       └── avatar_app/
│           └── home.html   # Bilingual table with PT/EN toggle
│
├── app.py                  # Data import + offline translation script
├── constants.py            # Translation dictionaries (lore, roles, places)
├── auditoria.py            # Script to audit untranslated terms in DB
├── manage.py
├── db.sqlite3
└── requirements.txt
```

---

## ⚙️ How It Works

### Data Flow

```
Last Airbender API
      │
      ▼
  app.py (fetch 497 characters)
      │
      ├─► PRIORIDADE_ALTA    ← exact match first (compound terms)
      ├─► DICIONARIO_AVATAR  ← lore terms, organizations
      ├─► NACOES             ← nations (Fire Nation → Nação do Fogo)
      ├─► LUGARES_AVATAR     ← locations (Ba Sing Se, Republic City...)
      ├─► CARGOS             ← roles (Soldier, Earthbender, Captain...)
      └─► PARENTESCO_AVATAR  ← family terms (Father, Sister...)
              │
              ▼
        Partial match engine
        (replaces known substrings, then cleans leftover connectives)
              │
              ▼
         SQLite DB
         (stores both PT and EN versions)
              │
              ▼
        Django views.py
        (orders: main cast first → secondary characters)
              │
              ▼
         home.html
         (live PT/EN toggle + search)
```

### Translation Strategy

The project uses a **100% offline, dictionary-based translation engine** — no external translation APIs required.

Translation priority order (highest to lowest):

1. `PRIORIDADE_ALTA` — compound terms and final corrections (e.g. `"Fire Nation music teacher"` → `"Professor de música da Nação do Fogo"`)
2. `DICIONARIO_AVATAR` — lore-specific terms and organizations
3. `NACOES` — the four nations and their variants
4. `LUGARES_AVATAR` — locations across both series
5. `CARGOS` — titles, roles, and bending disciplines
6. `PARENTESCO_AVATAR` — family relationships
7. Partial match fallback — substitutes known substrings left-to-right, longest match first
8. Connective cleanup — replaces leftover ` and ` → ` e `, ` or ` → ` ou `
9. Original preserved — if nothing matches, the English original is kept

Both the translated (PT) and original (EN) versions are stored in the database, enabling the live language toggle.

---

## 📋 Requirements

```
Django==6.0.4
requests==2.33.1
google-genai>=1.0.0       # optional — only needed if re-enabling AI translation
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/youruser/avatar_7_days.git
cd avatar_7_days
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Windows (bash)
source .venv/Scripts/activate

# Linux / Mac
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Import characters

```bash
python app.py
```

> Fetches ~497 characters from the [Last Airbender API](https://last-airbender-api.fly.dev), translates them offline, and populates the database. Takes ~30 seconds.

### 6. Start the server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## 🖥 CLI Usage

### Import / re-import all characters

```bash
python app.py
```

### Clear the database and reimport from scratch

```bash
python manage.py shell -c "from avatar_app.models import Personagem; Personagem.objects.all().delete(); print('DB cleared.')" && python app.py
```

### Audit untranslated terms in the database

```bash
python auditoria.py
```

Outputs a report like:

```
============================================================
NAMES in English (0):

AFFILIATIONS in English (2):
  - Acólito do Ars Official Avatar Aang Fan Club
  - ...

ALLIES in English (0):

ENEMIES in English (0):

TOTAL terms to fix: 2
============================================================
```

### Django admin

```bash
python manage.py createsuperuser
python manage.py runserver
# then visit http://127.0.0.1:8000/admin
```

---

## 🌐 Web Interface

Visit `http://127.0.0.1:8000` after starting the server.

### Features

| Feature | Description |
|---|---|
| 🇧🇷 / 🇺🇸 Toggle | Switch between Portuguese and English instantly — no page reload |
| 🔍 Live Search | Filters characters in real-time, respects current language |
| ⭐ Priority ordering | Main cast (Aang, Korra, Zuko, etc.) always appear at the top |
| 📷 Character photos | Loaded from the original API CDN with graceful fallback |
| 📱 Responsive | Works on mobile and desktop via Bootstrap 5 |

### Character priority list

The following characters are always shown first:

> Aang, Katara, Sokka, Toph, Zuko, Iroh, Azula, Appa, Momo, Suki, Ozai, Pakku, Bumi, Jet, Mai, Ty Lee, Ursa, Hakoda, Yue, Roku, Toph Beifong, Korra, Mako, Bolin, Asami, Tenzin, Lin, Amon, Zaheer, Kuvira, Tarrlok, Unalaq, Jinora, Ikki, Meelo, Varrick, Zhu Li, Suyin, Opal, Desna, Eska

To modify the list, edit `PERSONAGENS_PRINCIPAIS` in `avatar_app/views.py`.

---

## 🌍 API

The project fetches data from the public **Last Airbender API**:

```
GET https://last-airbender-api.fly.dev/api/v1/characters?perPage=1000
```

**Response fields used:**

| Field | Description |
|---|---|
| `name` | Character name |
| `affiliation` | Nation / organization affiliation |
| `allies` | List of allied characters |
| `enemies` | List of enemy characters |
| `photoUrl` | Character photo URL |

No API key required. The API is public and free.

---

## 🔧 Configuration

### Adding new translations

Edit `constants.py`. For compound terms or corrections, add to `PRIORIDADE_ALTA` (checked first):

```python
PRIORIDADE_ALTA = {
    # ...existing entries...
    "Your English term": "Sua tradução em português",
}
```

For simple roles or titles, add to `CARGOS`:

```python
CARGOS = {
    # ...existing entries...
    "Blacksmith": "Ferreiro",
}
```

After editing `constants.py`, re-run the import to apply changes:

```bash
python manage.py shell -c "from avatar_app.models import Personagem; Personagem.objects.all().delete(); print('DB cleared.')" && python app.py
```

### Changing main characters order

Edit `PERSONAGENS_PRINCIPAIS` in `avatar_app/views.py`:

```python
PERSONAGENS_PRINCIPAIS = [
    "Aang", "Katara", "Sokka",
    # add or remove names here
]
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Character data is sourced from the [Last Airbender API](https://last-airbender-api.fly.dev) — an unofficial, community-maintained resource. Avatar: The Last Airbender and The Legend of Korra are properties of Nickelodeon / Viacom.

---

<p align="center">
  Made with 🔥💧🌍💨 by Jerônimo
</p>
