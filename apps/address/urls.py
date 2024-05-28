from rest_framework.routers import DefaultRouter
from rest_framework_mongoengine.routers import DefaultRouter

from .viewsets.city import CityViewSet
from .viewsets.country import CountryViewSet
from .viewsets.state import StateViewSet

app_name = "address"

router = DefaultRouter()
router.register("country", CountryViewSet, basename="country")
router.register("state", StateViewSet, basename="state")
router.register("city", CityViewSet, basename="city")

urlpatterns = []
urlpatterns += router.urls
