import logging
from enum import Enum

import requests
from django.conf import settings
from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


class Command(str, Enum):
    GET_UPDATES = 'getUpdates'
    SEND_MESSAGE = 'sendMessage'


class TgClient:
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.BOT_TOKEN

    def get_url(self, method: str) -> str:
        print(method)
        return f"https://api.telegram.org/bot{self.token}/{method}"


    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
        print(**data)
        print(GetUpdatesResponse(**data))
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text)
        print(**data)
        print(SendMessageResponse(**data))
        return SendMessageResponse(**data)

    def _get(self, command: Command, **params) -> dict:
        url = self.get_url(command)
        response = requests.get(url, params=params)
        print(response.json())
        if not response.ok:
            print(response.json())
            raise ValueError
        return response.json()