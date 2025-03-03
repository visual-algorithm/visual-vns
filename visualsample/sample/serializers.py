from rest_framework import serializers
from .models import City, Salesman, Route

class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesman
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    salesman = SalesmanSerializer(read_only=True)
    salesman_id = serializers.PrimaryKeyRelatedField(
        queryset=Salesman.objects.all(), source='salesman', write_only=True
    )

    class Meta:
        model = City
        fields = ['id', 'name', 'salesman', 'salesman_id']

class RouteSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)
    cities_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), many=True, source='cities', write_only=True
    )
    salesmen = SalesmanSerializer(many=True, read_only=True)
    salesmen_id = serializers.PrimaryKeyRelatedField(
        queryset=Salesman.objects.all(), many=True, source='salesmen', write_only=True
    )

    class Meta:
        model = Route
        fields = ['id', 'name', 'cities', 'cities_id', 'salesmen', 'salesmen_id']
