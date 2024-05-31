from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_mongoengine.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.userauth.viewsets.user_login import CustomAuthTokenView, LogoutView

from .viewsets.user import UserViewset

app_name = "userauth"

router = DefaultRouter()
router.register("user", UserViewset, basename="user")

urlpatterns = [
    path("login/", CustomAuthTokenView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="token_blacklist"),
]
urlpatterns += router.urls
