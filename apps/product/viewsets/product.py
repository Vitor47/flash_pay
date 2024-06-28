# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.core.pagination import PageLimitPagination
from apps.core.permission import ProductPermission

from ..models import Product
from ..serializers.product import ProductRetrieveSerializer, ProductSerializer


class ProductViewset(ModelViewSet):

    """
    A viewset that provides the standard actions
    """

    permission_classes = (ProductPermission,)

    descriptor = {
        "POST": "Adicionou uma barraca.",
        "PUT": "Editou uma barraca.",
        "DELETE": "Removeu uma barraca.",
    }
    default_serializer_class = ProductSerializer
    pagination_class = PageLimitPagination
    serializer_classes = {
        "create": ProductSerializer,
        "update": ProductSerializer,
        "retrieve": ProductRetrieveSerializer,
        "list": ProductRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    def get_queryset(self):
        return Product.objects.filter(
            registered_by=self.request.user
        ).order_by("-id")

    def get_object(self):
        obj = super().get_object()

        if obj.registered_by != self.request.user:
            raise NotFound({"detail: Produto não encontrado"}, code=404)

        return obj

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
                "detail": "Produto editado com sucesso!",
                "university": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Produto deletado com sucesso!"},
            status=status.HTTP_200_OK,
        )
