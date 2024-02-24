from __future__ import annotations

from dataclasses import dataclass

from environs import Env
from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password,
    port, etc.

    Attributes
    ----------
    host : str
        The host where the db server is located.
    password : str
        The password used to authenticate with the db.
    user : str
        The username used to authenticate with the db.
    database : str
        The name of the db.
    port : int
        The port where the db server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def construct_sqlalchemy_url(
        self, driver: str = "asyncpg", host: str = None, port: int = None
    ) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this hhj configuration.

        :param driver: The name of the hhj driver (default is "asyncpg").
        :param host: The host for the connection.
        :param port: The port for the connection.
        :return: A SQLAlchemy connection URL as a string.
        """
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )

        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        """
        Creates a database configuration object.

        :param env: An Env object containing environment settings.
        :return: A database configuration object.
        """
        host = env.str("POSTGRES_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("POSTGRES_PORT", 5432)

        return DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port,
        )


@dataclass
class TgBot:
    """
    Telegram bot configuration class.
    This class holds the settings for the token, admins, groups, etc.

    Attributes
    ----------
    token : str
        The token received from BotFather.
    youth_policy: int
        The representing youth policy chat id.
    psychologist_support: int
        The representing psychologist_support chat id.
    legal_support: int
        The representing legal_support chat id.
    civic_education: int
        The representing civic_education chat id.
    living_library: int
        The representing living_library chat id.
    living_library_url: str
        The url of the living library.
    living_library_username: str
        The username of the living library.
    super_admin: int
        The representing super_admin id.
    admins: List[int]
        A list of user IDs representing the administrators of the bot.
    all_groups: List[int]
        A list of group chat IDs that the bot is connected to.
    """

    token: str
    youth_policy: int
    psychologist_support: int
    legal_support: int
    civic_education: int
    living_library: int
    living_library_url: str
    living_library_username: str
    super_admin: int
    admins: list[int]
    all_groups: list[int]

    @staticmethod
    def from_env(env: Env):
        """
        Creates a Telegram bot configuration object.

        :param env: An Env object containing environment settings.
        :return: A Telegram bot configuration object.
        """
        token = env.str("BOT_TOKEN")
        youth_policy = env.int("YOUTH_POLICY")
        psychologist_support = env.int("PSYCHOLOGIST_SUPPORT")
        legal_support = env.int("LEGAL_SUPPORT")
        civic_education = env.int("CIVIC_EDUCATION")
        living_library = env.int("LIVING_LIBRARY")
        living_library_url = env.str("LIVING_LIBRARY_URL")
        living_library_username = env.str("LIVING_LIBRARY_USERNAME")
        super_admin = env.int("SUPER_ADMIN")
        admins = list(map(int, env.list("ADMINS")))
        all_groups = list(map(int, env.list("GROUPS")))

        return TgBot(
            token=token,
            youth_policy=youth_policy,
            psychologist_support=psychologist_support,
            legal_support=legal_support,
            civic_education=civic_education,
            living_library=living_library,
            living_library_url=living_library_url,
            living_library_username=living_library_username,
            super_admin=super_admin,
            admins=admins,
            all_groups=all_groups,
        )


@dataclass
class Config:
    """
    Config configuration class
    This class holds the settings for config.

    Attributes
    ----------
    tg_bot: TgBot
        The Telegram bot configuration object
    db: DbConfig
        The db configuration object
    """

    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None) -> Config:
    """
    Loads the application configuration from an environment file and creates
    a Config object.

    :param path: Path to the environment file (default is None).
    :return: A config configuration object.
    """
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot.from_env(env), db=DbConfig.from_env(env))
