from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class OpenAIKEY:
    key: str


@dataclass
class TelegramBot:
    tg_bot_token: str


@dataclass
class RedisStorage:
    # для пользования на локальной машине
    port: int
    host: Union[int, str]


@dataclass
class Config:
    bot: TelegramBot
    chatGPT: OpenAIKEY
    redis_storage: RedisStorage


def load_bot_config(path) -> Config:
    env: Env = Env()
    env.read_env(path)
    bot = TelegramBot(tg_bot_token=env("BOT_TOKE"))
    redis = RedisStorage(port=env("REDIS_PORT"), host=env("REDIS_HOST"))
    open_ai_key = OpenAIKEY(key=env("OPENAI_API_KEY"))

    return Config(
        bot=bot,
        chatGPT=open_ai_key,
        redis_storage=redis, )
