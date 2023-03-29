from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def get_tasks(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(user=tg_user.user)
        if goals.count() > 0:
            response = [f"#{item.id} {item.title}" for item in goals]
            self.tg_client.send_message(msg.chat.id, "\n".join(response))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if tg_user.user:
            self.handle_authorized(tg_user, msg)
        else:
            self.handle_unauthorized(tg_user, msg)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_unauthorized(self, tg_user: TgUser, msg: Message):
        self.tg_client.send_message(msg.chat.id, 'Hello!')
        code = tg_user.set_verification_code()
        self.tg_client.send_message(tg_user.chat_id, f"verification code: {code}")

    def handle_authorized(self, tg_user: TgUser, msg: Message):
        if not msg.text:
            return
        if "/goals" in msg.text:
            self.get_tasks(msg, tg_user)
        else:
            self.tg_client.send_message(msg.chat.id, "[unknown command]")

    def create_goal(self, user, tg_user):
        categories = GoalCategory.objects.all()
        cat_text = ''
        for cat in categories:
            cat_text += f'{cat.id}: {cat.title} \n'

        self.tg_client.send_message(chat_id=tg_user.chat_id, text=f'Выберите категорию:\n{cat_text}')
        category = self.get_answer(tg_user.chat_id)

        self.tg_client.send_message(chat_id=tg_user.chat_id, text='Введите заголовок для цели')
        title = self.get_answer(tg_user.chat_id)

        result = Goal.objects.create(title=title, category=GoalCategory.objects.get(id=category), user=user, status=1,
                                     priority=1)
        return result.pk

    def get_answer(self, chat_id):
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                answer = item.message.text
                if item.message.chat.id == chat_id:
                    return answer
                else:
                    self.handle_message(item.message)