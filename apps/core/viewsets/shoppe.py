# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.core.pagination import PageLimitPagination
from apps.core.permission import (
    IsActivePermission,
    IsAdminPermission,
    IsTokenValid,
    IsTypeAdministradorPermission,
)

from ..models import Shoppe
from ..serializers.shoppe import ShoppeSerializer


class ShoppeViewset(ModelViewSet):

    """
    A viewset that provides the standard actions
    """

    permission_classes = (
        IsTokenValid,
        IsActivePermission,
        IsAdminPermission,
        IsTypeAdministradorPermission,
    )

    descriptor = {
        "POST": "Adicionou uma barraca.",
        "PUT": "Editou uma barraca.",
        "DELETE": "Removeu uma barraca.",
    }
    default_serializer_class = ShoppeSerializer
    pagination_class = PageLimitPagination
    serializer_classes = {
        "create": ShoppeSerializer,
        "update": ShoppeSerializer,
        "retrieve": ShoppeSerializer,
        "list": ShoppeSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    def get_queryset(self):
        return Shoppe.objects.filter(registered_by=self.request.user).order_by(
            "-id"
        )

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
                "detail": "Barraca / Café editado com sucesso!",
                "university": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Barraca / Café deletado com sucesso!"},
            status=status.HTTP_200_OK,
        )
