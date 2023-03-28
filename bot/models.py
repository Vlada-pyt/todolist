import os
import random
from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=350, null=True, blank=True, default=None)
    user = models.ForeignKey("core.User", models.PROTECT, null=True, blank=True, default=None)

    verification_code = models.CharField(max_length=35, default=None, null=True, blank=True)

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"

    @staticmethod
    def _generate_verification_code():
        return os.urandom(12).hex()

    def set_verification_code(self):
        code = self._generate_verification_code()
        self.verification_code = code
        self.save(update_fields=('verification_code',))

        return code

