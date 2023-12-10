import logging
from dataclasses import dataclass

from environs import Env
from sqlalchemy.engine import URL


@dataclass()
class TgBot:
    token: str
    name: str
    admin_ids: tuple[int]


@dataclass()
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def sqlalchemy_url(self) -> str:
        return str(URL.create(
            'postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )

        )


@dataclass
class Miscellaneous:
    log_level: str
    time_zone: str


@dataclass
class UserBot:
    api_id: int
    api_hash: str
    session_name: str


@dataclass
class Config:
    bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    userbot: UserBot

    @classmethod
    def from_env(cls, path: str = None) -> 'Config':
        env = Env()
        env.read_env(path)

        return Config(
            bot=TgBot(
                token=env.str('BOT_TOKEN'),
                admin_ids=tuple(map(int, env.list('ADMIN_IDS'))),
                name=env.str('BOT_NAME'),
            ),
            db=DbConfig(
                host=env.str('DB_HOST', 'localhost'),
                port=env.int('DB_PORT', 5432),
                user=env.str('DB_USER', 'postgres'),
                password=env.str('DB_PASS', 'postgres'),
                database=env.str('DB_NAME', 'postgres')
            ),
            userbot=UserBot(
                api_id=env.int('API_ID'),
                api_hash=env.str('API_HASH'),
                session_name=env.str('SESSION_NAME')
            ),
            misc=Miscellaneous(log_level=env.str('LOG_LEVEL', logging.INFO),
                               time_zone=env.str('TOME_ZONE', 'Europe/Kiev'))
        )
