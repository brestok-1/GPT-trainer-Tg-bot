import os
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(tg_bot=TgBot(token=os.getenv('BOT_TOKEN')))


PAGE_SIZE = 1050

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("API_KEY")}'
}