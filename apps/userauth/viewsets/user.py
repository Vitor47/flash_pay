# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.core.pagination import PageLimitPagination
from apps.core.permission import CustomUserPermission

from ..models import User
from ..serializers.change_password import ChangePasswordSerializer
from ..serializers.user import UserSerializer, UsuarioRetrieveMixinSerializer


class UserViewset(ModelViewSet):

    """
    A viewset that provides the standard actions
    """

    permission_classes = (CustomUserPermission,)

    descriptor = {
        "POST": "Adicionou um usuário.",
        "PUT": "Editou um usuário.",
        "DELETE": "Removeu um usuário.",
    }
    default_serializer_class = UserSerializer

    serializer_classes = {
        "create": UserSerializer,
        "update": UserSerializer,
        "retrieve": UsuarioRetrieveMixinSerializer,
        "list": UsuarioRetrieveMixinSerializer,
        "destroy": UserSerializer,
        "change_password": ChangePasswordSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    pagination_class = PageLimitPagination

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance = self.get_object()

        return Response(
            {
                "detail": "Usuário editado com sucesso!",
                "user": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Usuário deletado com sucesso!"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["PUT"], url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            {
                "detail": "Senha alterada com sucesso!",
                "usuario": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )
