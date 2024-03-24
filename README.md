# 🤖 Volunteer bot in Telegram 📱

A bot created to provide support and utility knowledge aimed at your personal development and adaptation in modern times society. There are four key areas and by choosing each one you will discover opportunity to get information and ask questions to our qualified volunteer experts.

## System dependencies

- Python 3.11+

- Docker
- docker-compose
- make

## Deployment

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Th3Kanashii/telegram-volunteer-bot.git
    ```

2. **Rename `.env.dist` to `.env` and configure it:**

   Rename the `.env.dist` file to `.env` and specify the necessary parameters for the bot to work.

3. **Build the application and run the bot:**

    Execute the following commands:

    ```bash
    make app-build
    make app-run
    ```

## Development

### Setup environment

```bash
make install
```

### Update database tables structure

**Make migration script:**

```bash
make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES rev_id=ID_MIGRATION
```

**Run migrations:**

```bash
make migrate
```

## Used technologies

- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram Bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
- [APScheduler](https://apscheduler.readthedocs.io/en/3.x/) (function scheduler)
