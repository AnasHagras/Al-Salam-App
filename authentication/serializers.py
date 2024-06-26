from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from django.contrib.auth import authenticate, login
from knox.models import AuthToken
from .models import LoginOTP


class RegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    phone_number = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "phone_number",
            "password",
            "password2",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            # email=validated_data["email"],
            phone_number=validated_data["phone_number"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label=_("phone_number"), write_only=True)

    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        user = None
        if phone_number and password:
            user = authenticate(request=self.context.get("request"), phone_number=phone_number, password=password)

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

        else:
            msg = _('Must include "phone_number" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class LoginOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        otp = attrs.get("otp")
        user = None
        if not phone_number or not otp:
            msg = _("Both phone number and OTP are required.")
            raise serializers.ValidationError(msg, code="authorization")
        otp_obj = LoginOTP.objects.filter(user__phone_number=phone_number, otp=otp).last()
        if not otp_obj:
            msg = _("OTP not found.")
            raise serializers.ValidationError(msg, code="authorization")
        if otp_obj.is_expired:
            otp_obj.delete()
            msg = _("OTP has expired.")
            raise serializers.ValidationError(msg, code="authorization")
        if otp_obj.otp != otp:
            msg = _("Invalid OTP.")
            raise serializers.ValidationError(msg, code="authorization")
        user = User.objects.get(phone_number=phone_number)
        attrs["otp_obj"] = otp_obj
        attrs["user"] = user
        return attrs

    def login(self):
        user = self.validated_data["user"]
        token = AuthToken.objects.create(user)
        login(self.context.get("request"), user)
        self.validated_data["otp_obj"].delete()
        return user, token[1]
