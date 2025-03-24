from rest_framework import serializers
from .models import Route, City, Salesman, Tmp
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class SalesmanSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Salesman
        fields = ['uuid', 'name', 'description', 'created_by', 'created_at', 'updated_at']

class CitySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    salesman = SalesmanSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['uuid', 'name', 'address', 'salesman', 'description', 'created_by', 'created_at', 'updated_at']

class RouteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    cities = CitySerializer(many=True, read_only=True)
    salesmen = SalesmanSerializer(many=True, read_only=True)
    depot = CitySerializer(read_only=True)

    class Meta:
        model = Route
        fields = ['uuid', 'name', 'depot', 'cities', 'salesmen', 'description', 'created_by', 'created_at', 'updated_at']

