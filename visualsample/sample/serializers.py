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
        # fields = ['id', 'name', 'salesman', 'salesman_id']
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all())
    salesmen = serializers.PrimaryKeyRelatedField(many=True, queryset=Salesman.objects.all())

    class Meta:
        model = Route
        fields = '__all__'
