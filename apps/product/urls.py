from rest_framework.routers import DefaultRouter
from rest_framework_mongoengine.routers import DefaultRouter

from .viewsets.category import CategoryViewset
from .viewsets.product import ProductViewset

app_name = "product"

router = DefaultRouter()
router.register("category", CategoryViewset, basename="category")
router.register("product", ProductViewset, basename="product")

urlpatterns = []
urlpatterns += router.urls
