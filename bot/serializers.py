from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='chat_id', read_only=True)
    # username = serializers.PrimaryKeyRelatedField(source='username', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'verification_code', 'user_id')
        read_only_fields = ('tg_id', 'user_id')

    def validate(self, code: str) -> str:
        self.tg_user = TgUser.objects.get(verification_code=code)
        if not self.tg_user:
            raise ValidationError({"verification_code": "field is incorrect"})
        return code

    def update(self, instance: TgUser, validated_data: dict):
        return self.tg_user
























