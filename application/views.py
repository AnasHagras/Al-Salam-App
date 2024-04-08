from django.shortcuts import render
from .models import Application
from rest_framework import generics
from .serializers import ApplicationSerializer
from rest_framework import permissions
from knox.auth import TokenAuthentication


class ApplicationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        print("APP : ", Application.objects.first())
        return Application.objects.first()
