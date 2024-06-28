# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.core.pagination import PageLimitPagination
from apps.core.permission import CategoryPermission

from ..models import Category
from ..serializers.category import CategorySerializer


class CategoryViewset(ModelViewSet):

    """
    A viewset that provides the standard actions
    """

    permission_classes = (CategoryPermission,)

    descriptor = {
        "POST": "Adicionou uma categoria.",
        "PUT": "Editou uma categoria.",
        "DELETE": "Removeu uma categoria.",
    }
    default_serializer_class = CategorySerializer
    pagination_class = PageLimitPagination
    serializer_classes = {
        "create": CategorySerializer,
        "update": CategorySerializer,
        "retrieve": CategorySerializer,
        "list": CategorySerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    def get_queryset(self):
        filter_query = Q()
        if self.request.user.type_user != "administrador":
            filter_query = Q(registered_by=self.request.user)

        return Category.objects.filter(filter_query).order_by("-id")

    def get_object(self):
        obj = super().get_object()

        if obj.registered_by != self.request.user:
            raise NotFound({"detail: Categoria não encontrado"}, code=404)

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
                "detail": "Categoria editada com sucesso!",
                "university": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Categoria deletada com sucesso!"},
            status=status.HTTP_200_OK,
        )
