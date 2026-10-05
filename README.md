# QuestForge

QuestForge is a Django application for managing tabletop fantasy campaigns. Game masters can organize a campaign and its characters, items, quests, monsters, and private notes. Players can browse campaigns, join with a character, manage their character’s details, and chat with the community in the Tavern.

For the app structure and entity relationships, see [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).

## Features

- Browse and search campaigns, items, quests, and monsters.
- Create campaigns and manage them as the game master.
- Join a campaign as a player.
- Game masters can add campaign-specific items, quests, and monsters, using the reusable catalogs as a starting point.
- Game masters can keep private campaign notes for their own reference.
- A player can create only one character per campaign, and ended campaigns cannot be joined.
- Players can leave a campaign by confirming deletion of their character.
- Visit the Tavern to read community messages; signed-in users can post, edit, and delete their own messages.
- View profiles, created campaigns, joined campaigns, and characters.
- See community and campaign counts on the home page.

## Tech stack

- Python 3.10 or newer
- Django 5.2
- SQLite by default
- Django templates, Bootstrap 4.5, and project JavaScript in `static/js/`

## Run locally

From the repository root, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies, create the database tables, and start the development server:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> for the home page. Campaigns are listed at <http://127.0.0.1:8000/campaigns/>.

Run the project test suite with:

```bash
python manage.py test
```

## Load the sample fixture

The repository includes `fixtures/db.json`, a snapshot of the current local database. Start with an empty or freshly migrated database, then load the fixture:

```bash
python manage.py migrate
python manage.py loaddata fixtures/db.json
```

The fixture includes the test accounts below. Loading it into a database that already contains records with the same primary keys can cause conflicts; use a fresh local database for a clean restore.

### Test accounts

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin` | `ghblehrb12` |
| Regular user | `Grob` | `ghblehrb12` |

These credentials are for local development and testing only.

## Main pages

| URL | Description |
| --- | --- |
| `/` | Home page and community counts |
| `/accounts/` | Registration, login, profiles, and account pages |
| `/campaigns/` | Campaign list, search, creation, and details |
| `/tavern/` | Community message feed and chat |
| `/items/` | Reusable item catalog |
| `/quests/` | Reusable quest catalog |
| `/monsters/` | Reusable monster catalog |
| `/hello-there/admin/` | Django administration site |

Campaign-specific characters and content are reached from campaign pages. Only the game master can update or delete the campaign and manage its items, quests, monsters, and private notes. Players need an account to join a campaign.

## Registration and email

New registrations create inactive accounts. The activation link is printed to the development server console; email delivery is not configured.

## Configuration

Settings are in `core/settings.py`. The checked-in configuration is for local development and is not suitable for production. Configure secure production settings before deployment.
