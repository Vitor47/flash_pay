# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from ..models import User


class CustomTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)

        user = User.objects.filter(email=attrs["email"]).first()
        if not user:
            raise serializers.ValidationError({"detail": "Login inválido!"})

        if not check_password(attrs["password"], user.password):
            raise serializers.ValidationError({"detail": "Login inválido!"})

        attrs["user"] = user

        return attrs
