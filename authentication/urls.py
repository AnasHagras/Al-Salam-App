from django.urls import path, include
from .views import Login, Register, GetCurrentUser, PerformLogin
from knox import views as knox_views

urlpatterns = [
    path("login-otp/", Login.as_view(), name="knox-login"),
    path("login/", PerformLogin.as_view(), name="knox-login"),
    path("current-user/", GetCurrentUser.as_view(), name="get-current-user"),
    path("register/", Register.as_view(), name="knox-register"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("logout-all/", knox_views.LogoutAllView.as_view(), name="logout-all"),
]
