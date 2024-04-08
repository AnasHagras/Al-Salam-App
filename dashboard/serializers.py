from rest_framework import serializers
from .models import Company, Slider


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = "__all__"
