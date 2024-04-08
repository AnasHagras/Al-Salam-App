from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _
from users.models import User
from rest_framework import generics
from .models import Company, Slider
from .serializers import CompanySerializer, SliderSerializer
from rest_framework import permissions
from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from utils.pagination import CustomNumberPagination


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
