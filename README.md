# QuestForge

QuestForge is a Django application for managing tabletop fantasy campaigns. Game masters can organize campaigns, characters, items, quests, monsters, and private campaign notes. Players can discover campaigns, join with a character, manage their profile, and talk with the community in the Tavern.

The deployed application is available at <https://questforge-l9d4.onrender.com/>. See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the app structure, data relationships, permissions, and deployment configuration.

## Features

- Browse campaigns and the Compendium's reusable items, quests, monsters, and spells.
- Create campaigns and manage them as the game master.
- Add campaign-specific items, quests, and monsters from reusable catalogs.
- Look up spell rules and class availability in the Compendium.
- Keep campaign notes visible only to the game master.
- Join a campaign with one character per player; ended campaigns cannot be joined.
- View profiles, campaigns, and characters associated with a user.
- Read and post messages in the site-wide Tavern.
- View campaign and player counts on the home page.

## Tech stack

- Python 3.10 or newer
- Django 5.2
- SQLite for development; PostgreSQL for the provided production settings
- Django templates, Bootstrap 4.5, and project JavaScript in `static/js/`
- WhiteNoise for serving collected static files

## Local development

From the repository root, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies, apply migrations, and run the local development server:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

`manage.py` defaults to `core.settings.dev`, which uses SQLite and enables Django debug mode. Open <http://127.0.0.1:8000/> for the home page. Campaigns are listed at <http://127.0.0.1:8000/campaigns/>.

Run the project tests with:

```bash
python manage.py test
```

## Sample database fixture

The repository includes `fixtures/db.json`, a snapshot of the local sample database. Apply migrations before loading it into a fresh development database:

```bash
python manage.py migrate
python manage.py loaddata fixtures/db.json
```

The fixture contains the development accounts below. Use a fresh local database to avoid primary-key conflicts.

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin` | `ghblehrb12` |
| Regular user | `Grob` | `ghblehrb12` |

These credentials are for local development and testing only. Do not load this fixture or use these credentials in a public or production environment.

## Main pages

| URL | Description |
| --- | --- |
| `/` | Home page and community counts |
| `/accounts/` | Registration, login, profiles, and account pages |
| `/campaigns/` | Campaign list, search, creation, and details |
| `/tavern/` | Community message feed |
| `/compendium/` | Compendium index |
| `/compendium/items/` | Reusable item catalog |
| `/compendium/quests/` | Reusable quest catalog |
| `/compendium/monsters/` | Reusable monster catalog |
| `/compendium/spells/` | Spell reference |
| `/hello-there/admin/` | Django administration site |

Campaign-specific characters and content are managed from campaign pages. Only the game master can update or delete a campaign or manage its campaign-specific content and notes. Players must sign in to join a campaign.

## Settings and deployment

Settings are split across `core/settings/base.py`, `core/settings/dev.py`, and `core/settings/prod.py`. The local `manage.py` command defaults to `core.settings.dev`. Select `core.settings.prod` by setting `DJANGO_SETTINGS_MODULE` in the process environment before starting the application. The production settings use PostgreSQL and require these environment variables:

- `DJANGO_SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_DB_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`

`.env.sample` lists the expected variables. Copy it to `.env` for local environment-variable loading and replace each placeholder. The `DJANGO_SETTINGS_MODULE` selection must be present in the process environment before Django starts; setting it only in `.env` is too late for the current `manage.py`, WSGI, or ASGI startup defaults. The deployed service should use `core.settings.prod`.

The production settings build `ALLOWED_HOSTS` from Render's `RENDER_EXTERNAL_HOSTNAME` environment variable. If the service uses a custom domain, make sure that hostname is also allowed. Production settings enforce HTTPS redirects and secure session/CSRF cookies. The production secret key must be set through `DJANGO_SECRET_KEY`; do not rely on the development fallback in `base.py`.

WhiteNoise serves static assets collected under `STATIC_ROOT`. Build the production static directory after installing dependencies and selecting production settings:

```bash
python manage.py collectstatic --noinput
```

Repeat this when static assets change. `STATIC_ROOT` is `staticfiles/`; `static/` contains the source CSS and JavaScript.

## Deployment notes

- Registration currently creates accounts as active, while the activation view and email service are placeholders. Registration messaging refers to email activation, but no activation email is sent and the activation flow is not implemented.
- The production host allowlist uses Render's generated hostname; custom domains need to be allowed as well.
- The fixture credentials are public development data and must never be used in production.
