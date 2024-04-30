from rest_framework.permissions import BasePermission

from apps.userauth.models import RevokedToken


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
