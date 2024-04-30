from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_mongoengine.routers import DefaultRouter

schema_view = get_schema_view(
    openapi.Info(
        title="FLASHPAY API",
        default_version="v1",
        description="API APP - FLASHPAY",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="vitormateusmiolo@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("apps.userauth.urls")),
    # Login backend in redocs or swagger
    path(
        "api-swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api-redocs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-ui",
    ),
]

urlpatterns += router.urls
