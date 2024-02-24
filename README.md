# Personality

Personality is a Telegram bot created to provide support and useful
knowledge aimed at your personal development and adaptation in the modern
society.
There are four key areas, and by choosing each of them, you will discover
the opportunity to receive information and ask questions
to our qualified volunteer experts.

## System dependencies
- Python 3.11+
- Docker
- docker-compose
- make

# Deployment

## Via Docker
1. Rename `.env.dist` to `.env` and configure it
2. Run `make app-build` command then `make app-run` to start the bot

## Update database tables structure
**Make migration script:**

    make migration message=MESSAGE_WHAT_THE_MIGRATION_DOES

**Run migrations:**

    make migrate

# Used technologies:
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram Bot framework)
- [PostgreSQL](https://www.postgresql.org/) (database)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Project Fluent](https://projectfluent.org/) (modern localization system)
