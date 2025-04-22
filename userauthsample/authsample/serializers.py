from rest_framework import serializers
from .models import Salesman, City, Route, Solution
from django.contrib.auth.models import User

class SalesmanSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Salesman
        fields = ["uuid", "name", "description", "created_at", "updated_at", "created_by"]

class CitySerializer(serializers.ModelSerializer):
    salesman = SalesmanSerializer(read_only=True)
    salesman_id = serializers.UUIDField(write_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = City
        fields = '__all__'

    def create(self, validated_data):
        salesman_id = validated_data.pop('salesman_id')
        city = City.objects.create(salesman=Salesman.objects.get(uuid=salesman_id), **validated_data)
        return city
    


class RouteSerializer(serializers.ModelSerializer):
    depot = CitySerializer(read_only=True)
    depot_id = serializers.UUIDField(write_only=True)
    cities = CitySerializer(many=True, read_only=True)
    city_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    salesmen = SalesmanSerializer(many=True, read_only=True)
    salesman_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Route
        fields = '__all__'

    def create(self, validated_data):
        depot_id = validated_data.pop('depot_id')
        city_ids = validated_data.pop('city_ids', [])
        salesman_ids = validated_data.pop('salesman_ids', [])

        route = Route.objects.create(depot=City.objects.get(uuid=depot_id), **validated_data)
        route.cities.set(City.objects.filter(uuid__in=city_ids))
        route.salesmen.set(Salesman.objects.filter(uuid__in=salesman_ids))
        return route
    
    def update(self, instance, validated_data):
        depot_id = validated_data.pop('depot_id', None)
        city_ids = validated_data.pop('city_ids', None)
        salesman_ids = validated_data.pop('salesman_ids', None)

        if depot_id is not None:
            instance.depot = City.objects.get(uuid=depot_id)
        if city_ids is not None:
            instance.cities.set(City.objects.filter(uuid__in=city_ids))
        if salesman_ids is not None:
            instance.salesmen.set(Salesman.objects.filter(uuid__in=salesman_ids))

        return super().update(instance, validated_data)
    
class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user