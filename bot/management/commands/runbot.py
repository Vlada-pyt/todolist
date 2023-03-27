import json
import logging

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal, GoalCategory

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0
        logger.info('Bot started handling')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message, offset)
                logger.info(item.message)

    def _build_keyboard(self, items):
        keyboard = [[item.title] for item in items]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def handle_message(self, message: Message, offset):
        tg_user, created = TgUser.objects.get_or_create(chat_id=message.chat.id)

        logger.info(f'Created: {created}')

        if tg_user.user:
            self.handle_authorized(tg_user=tg_user, message=message, offset=offset)
        else:
            self.handle_unauthorized(tg_user=tg_user, message=message)

    def handle_unauthorized(self, message: Message, tg_user: TgUser):
        self.tg_client.send_message(chat_id=message.chat.id, text='Hello!')

        verification_code = tg_user.set_verification_code()

        self.tg_client.send_message(
            chat_id=tg_user.chat_id,
            text=f'Verification_code: {verification_code}'
        )

    def handle_authorized(self, tg_user: TgUser, message: Message, offset):
        if message.text not in ["/goals", "/create"]:
            self.tg_client.send_message(tg_user.chat_id, "command doesn't exist")
        if message.text == "/create":
            self.choice_category(tg_user=tg_user, offset=offset)
        elif message.text == "/goals":
            goals = Goal.objects.filter(
                category__board__participants__user=tg_user.user,
                category__is_deleted=False
            ).exclude(status=Goal.Status.archived)
            for goal in goals:
                self.tg_client.send_message(tg_user.chat_id, goal.title if goal.title else None)

    def choice_category(self, tg_user: TgUser, offset):
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user, is_deleted=False)
        keyboard = self._build_keyboard(categories)
        self.tg_client.send_message(tg_user.chat_id,
                                    f'Choose category from menu or type /cancel to cancel',
                                    reply_markup='{}'.format(keyboard)
                                    )
        dict_categories = {item.title: item for item in categories}

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=offset)
            for item in response.result:
                self.offset = item.update_id + 1
                if item.message.text in dict_categories:
                    category = dict_categories.get(item.message.text)
                    self.create_goal(tg_user, category=category, offset=self.offset)
                    flag = False
                elif item.message.text == '/cancel':
                    self.tg_client.send_message(tg_user.chat_id, 'Canceled goal creating')

    def create_goal(self, tg_user: TgUser, category: GoalCategory, offset: int = 0):
        self.tg_client.send_message(tg_user.chat_id, f'Type goal to add to category: {category.title}')

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=offset)
            for item in response.result:
                self.offset = item.update_id + 1

                goal = Goal.objects.create(
                    title=item.message.text,
                    category=category,
                    user=tg_user.user
                )
                flag = False

                self.tg_client.send_message(tg_user.chat_id, f"Goal {goal.title} is created")