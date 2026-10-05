# QuestForge project overview

QuestForge is a Django application for managing tabletop fantasy campaigns. It includes accounts and profiles, campaigns and characters, reusable catalogs for items, quests, and monsters, private game-master campaign notes, and a site-wide chat called the Tavern. The home page shows the current campaign and user counts.

## Application structure

```mermaid
flowchart LR
    Player[Player / game master] -->|browser request| Routes[core.urls]
    Routes --> Accounts[accounts app]
    Routes --> Campaigns[campaigns app]
    Routes --> Characters[characters app]
    Routes --> Items[items app]
    Routes --> Quests[quests app]
    Routes --> Monsters[monsters app]
    Routes --> Chats[chats app]

    Accounts --> Views[Views and app services]
    Campaigns --> Views
    Characters --> Views
    Items --> Views
    Quests --> Views
    Monsters --> Views
    Chats --> Views

    Views --> Models[Models and relationships]
    Models <--> Database[(SQLite in development / PostgreSQL in production settings)]
    Views --> Templates[HTML templates]
    Templates --> Browser[Rendered pages]
    CSS[static/css/styles.css] --> Browser
    JS[static/js/] --> Browser
    Browser --> Player
```

## Apps and data relationships

```mermaid
erDiagram
    USER ||--o| PROFILE : has
    USER ||--o{ CAMPAIGN : runs
    USER ||--o{ CAMPAIGN_NOTE : writes
    USER ||--o{ MESSAGE : posts
    USER ||--o{ CHARACTER : plays
    CAMPAIGN ||--o{ CHARACTER : includes
    CAMPAIGN ||--o{ CAMPAIGN_NOTE : has
    RACE ||--o{ CHARACTER : chooses
    CHARACTER_CLASS ||--o{ CHARACTER : chooses

    CAMPAIGN ||--o{ CAMPAIGN_ITEM : contains
    ITEM o|--o{ CAMPAIGN_ITEM : customizes
    CHARACTER }o--o{ CAMPAIGN_ITEM : carries

    CAMPAIGN ||--o{ CAMPAIGN_QUEST : contains
    QUEST o|--o{ CAMPAIGN_QUEST : customizes

    CAMPAIGN ||--o{ CAMPAIGN_MONSTER : contains
    MONSTER o|--o{ CAMPAIGN_MONSTER : customizes
```

`Item`, `Quest`, and `Monster` are reusable catalog entries. Campaign-specific versions can be customized for a particular campaign while retaining an optional link to the catalog entry. Each character belongs to one campaign and one player; a database constraint limits each player to one character per campaign.

Campaign notes are private to the game master. Only the campaign's game master can view or manage them. Joining a campaign requires authentication, and ended campaigns cannot be joined. Players leave by deleting their own character from the campaign.

The Tavern is a site-wide message feed. Anyone can read messages; authenticated users can post. Users can edit or delete only their own messages.

## Access rules

- Campaign creation requires login; the authenticated user is assigned as the game master by the server.
- Only the game master can update or delete a campaign or manage its campaign-specific items, quests, monsters, and notes.
- A player can have at most one character per campaign, enforced by a database constraint.
- Only authenticated users can join a campaign or post a Tavern message.
- A player can delete their own character to leave a campaign.
- Profile email is visible only to the profile owner.
- Tavern messages are public to read; only the author can edit or delete a message.

## Settings and deployment configuration

Settings are split into:

- `core/settings/base.py`: shared applications, middleware, templates, authentication, and static-file paths.
- `core/settings/dev.py`: local SQLite database and `DEBUG = True`.
- `core/settings/prod.py`: PostgreSQL connection from environment variables, `DEBUG = False`, and HTTPS redirects with secure session and CSRF cookies.

`manage.py` defaults to `core.settings.dev`. The WSGI and ASGI entry points default to `core.settings`; deployment must set `DJANGO_SETTINGS_MODULE=core.settings.prod` in the process environment before starting the application. The `.env.sample` file lists the database and secret-key variables used by the production settings. Its current `DJANGO_SETTINGS_MODULE` placeholder does not change the module selection when it is read only after Django startup begins.

The production settings currently allow only `127.0.0.1` and `localhost`; update `ALLOWED_HOSTS` for the deployment domain before launch. HTTPS redirect and secure-cookie settings assume the deployed site is served over correctly configured HTTPS. Review the settings for the target host and proxy before public deployment.

WhiteNoise middleware is configured immediately after Django's `SecurityMiddleware`. Source static assets are in `static/`, and collected assets are written to `staticfiles/` (`STATIC_ROOT`). Run the following with production settings during the deployment build, and whenever static assets change:

```bash
python manage.py collectstatic --noinput
```

`requirements.txt` includes Django, `python-dotenv`, PostgreSQL's psycopg2 driver, and WhiteNoise.

## Local database fixture

`fixtures/db.json` is a development snapshot. Restore it to a fresh local SQLite database after applying migrations:

```bash
python manage.py migrate
python manage.py loaddata fixtures/db.json
```

The fixture contains development accounts `admin` / `ghblehrb12` (administrator) and `Grob` / `ghblehrb12` (regular user). These credentials and data are for local testing only. Never use them in a public environment.

## Known pre-deployment limitations

- Registration currently creates active accounts. The activation view and email service are placeholders, although the registration message still instructs users to check email. Email delivery and account activation need implementation or the messaging needs to be revised.
- Production host names have not yet been configured; `ALLOWED_HOSTS` is currently localhost-only.
- Production startup requires `DJANGO_SETTINGS_MODULE=core.settings.prod` to be set outside the current `.env` loading path.

## Main pages

| URL area | What it contains |
| --- | --- |
| `/` | Home page and community counts |
| `/accounts/` | Registration, authentication, profiles, and account pages |
| `/campaigns/` | Campaign list, search, details, characters, and campaign-specific content |
| `/tavern/` | Public community message feed |
| `/items/` | Reusable item catalog |
| `/quests/` | Reusable quest catalog |
| `/monsters/` | Reusable monster catalog |
| `/hello-there/admin/` | Django administration site |

The site stylesheet is `static/css/styles.css`. Project JavaScript is kept in `static/js/` and loaded by templates that use it.
