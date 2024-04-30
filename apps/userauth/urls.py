from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_mongoengine.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.userauth.viewsets.user_login import CustomAuthTokenView, LogoutView

from .views import login_user, logout_user
from .viewsets.user import UserViewset

app_name = "userauth"

router = DefaultRouter()
router.register("api/user", UserViewset, basename="user")

urlpatterns = [
    path("api/login/", CustomAuthTokenView.as_view(), name="login"),
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", LogoutView.as_view(), name="token_blacklist"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
urlpatterns += router.urls
