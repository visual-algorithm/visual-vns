from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import City, Salesman, Route
from .serializers import CitySerializer, SalesmanSerializer, RouteSerializer

from algorithms.model import model

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class SalesmanViewSet(viewsets.ModelViewSet):
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer
    permission_classes = [AllowAny]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]

def send_result_for_ios(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # citiesにdepotは含まれます。
    cities = list(route.cities.all())
    salesmen = list(route.salesmen.all())
    salesman_names = []
    for city in cities:
        salesman_name = city.salesman.name
        salesman_names.append(str(salesman_name))

    depot_address = route.depot.address
    city_addresses = list(route.cities.values_list("address", flat=True))

    city_addresses.remove(depot_address)
    
    salesman_name_set = set(salesman_names)
    if 'Shared'in salesman_name_set:
        salesman_name_set.remove('Shared')
    salesman_name_list = list(salesman_name_set)
    exclusive_cities = [[] for i in range(len(salesmen)-1)]
    shared_cities = []
    for i in range(len(salesman_names)):
        if salesman_names[i] == 'shared' or salesman_names[i] == 'Shared':
            if i != 0:
                shared_cities.append(i)
        else:
            for j in range(len(salesman_name_list)):
                if salesman_names[i] == salesman_name_list[j]:
                    exclusive_cities[j].append(i)

    city_addresses.insert(0, depot_address)

    # print(depot_address)
    # print(city_addresses)
    # print(len(salesmen)-1)
    # print(exclusive_cities)
    # print(shared_cities)

    m = model(route_id, len(salesmen)-1, len(cities), city_addresses, exclusive_cities, shared_cities)

    m.get_data()

    context = {
        'html_name': str(route_id)+'.html',
    }
    return render(request, "restpractice/result_for_ios.html", context)