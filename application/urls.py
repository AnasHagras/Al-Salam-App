from django.urls import path
from .views import ApplicationSettingsView

urlpatterns = [
    path("app-settings/", ApplicationSettingsView.as_view(), name="application-settings"),
]
