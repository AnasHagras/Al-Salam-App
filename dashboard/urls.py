from django.urls import path
from .views import DashboardStatsView, CompanySettingsView

urlpatterns = [
    path("stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("company-settings/", CompanySettingsView.as_view(), name="company-settings"),
]
