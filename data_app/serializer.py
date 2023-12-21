from rest_framework import serializers
from .models import IndianCompany, LLPCompany, FCINCompany


class IndianCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndianCompany
        fields = '__all__'


class LLPCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = LLPCompany
        fields = '__all__'


class FCINCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = FCINCompany
        fields = '__all__'
