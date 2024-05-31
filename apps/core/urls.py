from rest_framework.routers import DefaultRouter
from rest_framework_mongoengine.routers import DefaultRouter

from .viewsets.shoppe import ShoppeViewset
from .viewsets.university import UniversityViewset

app_name = "core"

router = DefaultRouter()
router.register("university", UniversityViewset, basename="university")
router.register("shoppe", ShoppeViewset, basename="shoppe")

urlpatterns = []
urlpatterns += router.urls
