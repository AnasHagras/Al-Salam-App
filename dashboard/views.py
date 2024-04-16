from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _
from users.models import User
from rest_framework import generics
from .models import Company, Slider, Country, City
from .serializers import CompanySerializer, SliderSerializer, CountrySerializer, CitySerializer
from rest_framework import permissions
from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from utils.pagination import CustomNumberPagination
from users.serializers import UserSerializer
from utils.permissions import IsAdminUser
from .models import ContactUsMessage
from .serializers import ContactUsMessageSerializer


class DashboardStatsView(APIView):
    def get(self, request):
        total_users = User.objects.customers().count()
        return Response({"total_customers": total_users}, status=200)


class CompanySettingsView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return Company.objects.first()


class SliderView(ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomNumberPagination

    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    class Meta:
        ordering = ["id"]


class AdminUsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(phone_number__icontains=search)
        return queryset

    class Meta:
        ordering = ["id"]


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = None
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    class Meta:
        ordering = ["id"]


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = None

    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        if country:
            queryset = queryset.filter(country=country)
        return queryset

    class Meta:
        ordering = ["id"]


class ContactUsMessageViewSet(ModelViewSet):
    queryset = ContactUsMessage.objects.all()
    serializer_class = ContactUsMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post"]

    # def get_permissions(self):
    #     if self.request.method in ["POST"]:
    #         self.permission_classes = [permissions.IsAuthenticated]
    #     return super().get_permissions()
