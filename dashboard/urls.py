from django.urls import path, include
from .views import DashboardStatsView, CompanySettingsView, SliderView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"slider", SliderView, basename="slider")

urlpatterns = [
    path("", include(router.urls)),
    path("stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("company-settings/", CompanySettingsView.as_view(), name="company-settings"),
]
