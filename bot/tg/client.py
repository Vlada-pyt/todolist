from enum import Enum

import requests
from django.conf import settings

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


class Command(str, Enum):
    GET_UPDATES = 'getUpdates'
    SEND_MESSAGE = 'sendMessage'
    GET_GOALS = 'goals'
    CREATE_GOAL = 'create'


class TgClient:
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.BOT_TOKEN

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str, reply_markup=None) -> SendMessageResponse:
        if reply_markup:
            data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text, reply_markup=reply_markup)
        data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def _get(self, command: Command, **params) -> dict:
        url = self.get_url(command)
        response = requests.get(url, params=params)

        return response.json()
