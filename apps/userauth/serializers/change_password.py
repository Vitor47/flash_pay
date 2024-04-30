from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from apps.core.utils import is_password_valid


class ChangePasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    password_now = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirmed_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance

    def validate(self, attrs):
        attrs = super().validate(attrs)
        new_password = attrs.get("new_password")
        confirmed_password = attrs.get("confirmed_password")

        if new_password != confirmed_password:
            raise serializers.ValidationError(
                {"error": "As senhas não coincidem."}
            )

        if not is_password_valid(new_password):
            raise serializers.ValidationError(
                {"error": "A senha não é válida."}
            )

        if not check_password(attrs["password_now"], self.instance.password):
            raise serializers.ValidationError(
                {"error": "Senha atual incorreta."}
            )

        return attrs
