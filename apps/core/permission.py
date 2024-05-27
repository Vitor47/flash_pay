from rest_framework import permissions
from rest_framework.permissions import BasePermission

from apps.core.models import RevokedToken


class CustomUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True

        if not request.user.is_authenticated:
            return False

        elif view.action in [
            "list",
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "change_password",
        ]:
            id = view.kwargs.get("id")

            if str(request.user.id) == str(id) or request.user.admin:
                return True

        return False


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        # Se a requisição é do Swagger, permita
        if request.META.get("HTTP_REFERER", "").startswith("/api-swagger/"):
            return True

        user_id = request.user.id
        access_token = request.auth  # Token de acesso

        # Verifica se o token está na lista de tokens inválidos
        if RevokedToken.objects.filter(
            user=user_id, key=str(access_token)
        ).count():
            return False

        return True
