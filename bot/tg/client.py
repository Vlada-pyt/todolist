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
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        resp = requests.get(url, params={"offset": offset, "timeout": timeout})
        return GetUpdatesResponse(resp)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        resp = requests.post(url, json={"chat_id": chat_id, "text": text})
        return SendMessageResponse(resp)

    # def _get(self, command: Command, **params) -> dict:
    #     url = self.get_url(command)
    #     response = requests.get(url, params=params)
    #     if not response.ok:
    #         print(response.json())
    #         raise ValueError
    #     return response.json()