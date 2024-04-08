from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework import permissions, generics
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import login
from .serializers import LoginSerializer, RegisterSerializer, LoginOTPSerializer
from users.models import User
from rest_framework import status
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from utils.helpers import generateOTP, send_message_to_number
from .models import LoginOTP


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
        otp = generateOTP()
        login_otp, created = LoginOTP.objects.get_or_create(user=serializer.validated_data["user"])
        if login_otp.is_expired:
            login_otp = LoginOTP.objects.create(user=serializer.validated_data["user"], otp=otp)
        login_otp.otp = otp
        login_otp.save()
        send_message_to_number(serializer.validated_data["user"], otp)
        return Response(
            {
                "message": _("OTP has been successfully sent to your mobile number."),
            },
            status=200,
        )


class PerformLogin(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]
    serializer_class = LoginOTPSerializer

    def post(self, request):
        serializer = LoginOTPSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user, token = serializer.login()
        return Response(
            {"token": token, "user": UserSerializer(user).data, "message": "success"}, status=status.HTTP_200_OK
        )


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
