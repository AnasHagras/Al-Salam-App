from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _


class TestRender(APIView):
    def get(self, request):
        return Response({"message": _("Hello, {name} World!!!!").format(name="anas")}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
