from rest_framework import serializers
from .models import Company, Slider, Country, City


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"
