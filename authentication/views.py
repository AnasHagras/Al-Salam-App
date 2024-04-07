from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import permissions, generics
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import login
from .serializers import LoginSerializer, RegisterSerializer
from users.models import User
from rest_framework import status
from rest_framework.views import APIView
from django.utils.translation import gettext as _


class Login(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user, token = serializer.login()
        return Response({"token": token[1], "user": UserSerializer(user).data, "message": "success"}, status=200)


class GetCurrentUser(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, status=200)


class Register(generics.GenericAPIView):
    permission_classes = permissions.AllowAny
    serializer_class = RegisterSerializer
    authentication_classes = []
    lookup_field = User

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            },
            status=201,
        )
