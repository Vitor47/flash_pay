# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import RevokedToken
from apps.core.token.tokens import RefreshToken
from apps.log.models import AuditLog

from ..serializers.user_login import CustomTokenObtainSerializer


class CustomAuthTokenView(APIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = CustomTokenObtainSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Registro de auditoria
        ip_address: str = request.META.get("REMOTE_ADDR")
        AuditLog.objects.create(user=user, ip_address=str(ip_address))

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        exp_datetime = (
            datetime.utcnow() + settings.SIMPLE_JWT["JWT_EXPIRATION_DELTA"]
        )
        token_expiry = exp_datetime.strftime("%d/%m/%Y %H:%M:%S")

        # Create the token payload
        payload = {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "admin": user.admin,
                "type_user": user.type_user.title(),
            },
            "exp": token_expiry,
            "refresh": str(refresh),
            "access": str(access),
        }

        return Response(payload, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        try:
            user_id = request.user.id
            access_token = request.auth  # Token de acesso

            RevokedToken.create_revoked_token(user_id, access_token)
        except IntegrityError:
            return Response(
                {"detail": "Token está inátivo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Usuário deslogado com sucesso."},
            status=status.HTTP_200_OK,
        )
