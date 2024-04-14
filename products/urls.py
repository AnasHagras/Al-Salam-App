from django.urls import path, include
from .views import CategoryViewSet, UnitViewSet, ProductViewSet, ProductImagesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"unit", UnitViewSet, basename="unit")
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("assign-images-to-product/", ProductImagesView.as_view(), name="assign-images-to-product"),
]
