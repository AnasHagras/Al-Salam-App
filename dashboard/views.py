from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _
from users.models import User
from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
from rest_framework import permissions
from knox.auth import TokenAuthentication


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
