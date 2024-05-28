# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from apps.address.models import State
from apps.address.serializers.state import StateSerializer
from apps.core.pagination import PageLimitPagination


class StateViewSet(ModelViewSet):
    """
    A viewset that provides the standard actions
    """

    descriptor = {
        "POST": "Adicionou um estado.",
        "PUT": "Editou um estado.",
        "DELETE": "Removeu um estado.",
    }
    serializer_class = StateSerializer
    pagination_class = PageLimitPagination
    queryset = State.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        return super(StateViewSet, self).create(request, *args, **kwargs)

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
                "detail": "Estado editado com sucesso!",
                "pais": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(
            data={"detail": "Estado deletado com sucesso!"},
            status=status.HTTP_200_OK,
        )
