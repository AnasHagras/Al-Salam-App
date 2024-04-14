from django.urls import path, include
from .views import DashboardStatsView, CompanySettingsView, SliderView, AdminUsersViewSet, CountryViewSet, CityViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"slider", SliderView, basename="slider")
router.register(r"country", CountryViewSet, basename="Country")
router.register(r"city", CityViewSet, basename="city")
router.register(r"admin-users", AdminUsersViewSet, basename="admin-users")

urlpatterns = [
    path("", include(router.urls)),
    path("stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("company-settings/", CompanySettingsView.as_view(), name="company-settings"),
]
