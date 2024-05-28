# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.core.pagination import PageLimitPagination

from ..models import University
from ..serializers.university import UniversitySerializer


class UniversityViewset(ModelViewSet):

    """
    A viewset that provides the standard actions
    """

    descriptor = {
        "POST": "Adicionou uma universisade.",
        "PUT": "Editou uma universisade.",
        "DELETE": "Removeu uma universisade.",
    }
    default_serializer_class = UniversitySerializer

    serializer_classes = {
        "create": UniversitySerializer,
        "update": UniversitySerializer,
        "retrieve": UniversitySerializer,
        "list": UniversitySerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    pagination_class = PageLimitPagination

    def get_queryset(self):
        return University.objects.all().order_by("-id")

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
                "detail": "Faculdade / Universidade editado com sucesso!",
                "university": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Faculdade / Universidade deletado com sucesso!"},
            status=status.HTTP_200_OK,
        )
