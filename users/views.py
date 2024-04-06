from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


class TestRender(APIView):
    def get(self, request):
        return render(request, "templates/test.html")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
