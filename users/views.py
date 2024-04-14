from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
from rest_framework import permissions
from utils.permissions import IsAdminOrOwner


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # ! TO BE COMPLETED
