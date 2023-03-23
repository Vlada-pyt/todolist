from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='chat_id', read_only=True)
    # username = serializers.PrimaryKeyRelatedField(source='username',)

    class Meta:
        model = TgUser
        read_only_fields = ("tg_id", "user_id", "username")
        fields = ("tg_id", "verification_code", "user_id", "username")

    # def validate_verification_code(self, attrs):
    #     verification_code = attrs.get("verification_code")
    #     tg_user = TgUser.objects.filter(verification_code=verification_code).first()
    #     if not tg_user:
    #         raise ValidationError({"verification_code": "field is incorrect"})
    #     attrs["tg_user"] = tg_user
    #     return attrs
    def validate_verification_code(self, code: str) -> str:
        try:
            self.tg_user = TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise ValidationError('Field is incorrect')
        return code
    def update(self, instance: TgUser, validated_data: dict):
        return self.tg_user








