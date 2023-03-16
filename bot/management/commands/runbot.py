import logging

from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(tg_user.chat_id, 'Hello!')
        code = tg_user.set_verification_code()
        self.tg_client.send_message(tg_user.chat_id, f"verification code: {code}")

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        logger.info('Authorized')

    def get_tasks(self, msg: Message, tg_user: TgUser):
        goal = Goal.objects.filter(user=tg_user.user)
        if goal.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in goal]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return f"Can't be empty"
        if "/goals" in msg.text:
            self.get_tasks(msg, tg_user)
        else:
            self.tg_client.send_message(msg.chat.id, "[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)

        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle(self, *args, **kwargs):
        offset = 0

        logger.info('Bot start handling')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)





















