# from rest_framework import serializers
# from .models import City, Salesman, Route

from rest_framework import serializers
from .models import City, Salesman, Route, Solution

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['uuid', 'name', 'address', 'salesman', 'description', 'created_at', 'updated_at']

class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesman
        fields = ['uuid', 'name', 'description', 'created_at', 'updated_at']

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

    class Meta:
        model = Route
        fields = ['uuid', 'name', 'depot', 'depot_id', 'cities', 'city_ids', 'salesmen', 'salesman_ids', 'description', 'created_at', 'updated_at']

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


# class CitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = City
#         fields = '__all__'

# class SalesmanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Salesman
#         fields = '__all__'

# class RouteSerializer(serializers.ModelSerializer):
#     cities = CitySerializer(many=True, read_only=True)
#     city_ids = serializers.ListField(
#         child=serializers.UUIDField(), write_only=True, required=False
#     )

#     class Meta:
#         model = Route
#         fields = ['id', 'name', 'cities', 'city_ids']

#     def create(self, validated_data):
#         city_ids = validated_data.pop('city_ids', [])
#         route = Route.objects.create(**validated_data)
#         route.cities.set(City.objects.filter(id__in=city_ids))
#         return route

#     def update(self, instance, validated_data):
#         city_ids = validated_data.pop('city_ids', None)
#         if city_ids is not None:
#             instance.cities.set(City.objects.filter(id__in=city_ids))
#         return super().update(instance, validated_data)
