import os
import random
from django.db import models

from core.models import User
CODE_ITEMS = "gftecjguymzxcvbnmar567890"


class TgUser(models.Model):
    chat_id = models.BigIntegerField(default=None)
    tg_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=350, null=True, blank=True, default=None)
    user = models.ForeignKey("core.User", models.PROTECT, null=True, blank=True, default=None)

    verification_code = models.CharField(max_length=35, default=None)

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"

    def set_verification_code(self):
        code = "".join([random.choice(CODE_ITEMS) for _ in range(12)])
        self.verification_code = code
