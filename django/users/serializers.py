from rest_framework import serializers
from .models import User, Promocode, PromocodeUsage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = '__all__'

class PromocodeUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromocodeUsage
        fields = '__all__'
