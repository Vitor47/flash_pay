from rest_framework.routers import DefaultRouter
from rest_framework_mongoengine.routers import DefaultRouter

from .viewsets.university import UniversityViewset

app_name = "core"

router = DefaultRouter()
router.register("university", UniversityViewset, basename="university")

urlpatterns = []
urlpatterns += router.urls
