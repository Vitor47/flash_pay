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
        user_id = request.user.id
        access_token = request.auth  # Token de acesso

        # Verifica se o token está na lista de tokens inválidos
        if RevokedToken.objects.filter(
            user=user_id, key=str(access_token)
        ).count():
            return False

        return True


class IsActivePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.active:
            return False

        return True


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.admin:
            return False

        return True


class IsTypeAdministradorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.type_user != "administrador":
            return False

        return True


class IsTypeVendedorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.type_user != "vendedor":
            return False

        return True
