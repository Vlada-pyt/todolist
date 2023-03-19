from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='chat_id', read_only=True)
    username = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'verification_code', 'user_id', 'username')
        read_only_fields = ('tg_id', 'user_id')

    def validate(self, attrs):
        verification_code = attrs.get("verification_code")
        tg_user = TgUser.objects.filter(verification_code=verification_code)
        if not tg_user:
            raise ValidationError({"verification_code": "field is incorrect"})
        attrs["tg_user"] = tg_user
        return attrs

    # def update(self, instance: TgUser, validated_data: dict):
    #     return self.tg_user
























