# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.address.models import City
from apps.address.serializers.city import CitySerializer
from apps.core.pagination import PageLimitPagination


class CityViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """

    descriptor = {
        "POST": "Adicionou uma cidade.",
        "PUT": "Editou uma cidade.",
        "DELETE": "Removeu uma cidade.",
    }
    serializer_class = CitySerializer
    pagination_class = PageLimitPagination

    def get_queryset(self):
        return City.objects.all().order_by("-id")
    
    @method_decorator(cache_page(2400 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
                "detail": "Cidade editada com sucesso!",
                "pais": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Cidade deletada com sucesso!"},
            status=status.HTTP_200_OK,
        )
