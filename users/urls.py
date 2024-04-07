from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TestRender

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [path("", include(router.urls)), path("test/", TestRender.as_view())]
