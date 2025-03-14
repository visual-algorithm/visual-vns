from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Route, City, Salesman
from .serializers import RouteSerializer, CitySerializer, SalesmanSerializer

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from algorithms.vns_model import model

class SalesmanViewSet(viewsets.ModelViewSet):
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().select_related('salesman', 'created_by')
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().prefetch_related('depot', 'cities', 'salesmen', 'created_by')
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

def ex_solve(request, route_id):
    route = get_object_or_404(Route, uuid=route_id)
    context = {"route": route}
    return render(request, "result.html", context)

def solve(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    cities = list(route.cities.all())
    salesmen = list(route.salesmen.all())
    salesman_names = []
    for city in cities:
        salesman_name = city.salesman.name
        salesman_names.append(str(salesman_name))

    depot_address = route.depot.address
    city_addresses = list(route.cities.values_list("address", flat=True))
    
    salesman_name_set = set(salesman_names)
    if 'Shared'in salesman_name_set:
        salesman_name_set.remove('Shared')
    salesman_name_list = list(salesman_name_set)
    exclusive_cities = [[] for i in range(len(salesmen)-1)]
    shared_cities = []
    for i in range(len(salesman_names)):
        if salesman_names[i] == 'shared' or salesman_names[i] == 'Shared':
            shared_cities.append(i+1)
        else:
            for j in range(len(salesman_name_list)):
                if salesman_names[i] == salesman_name_list[j]:
                    exclusive_cities[j].append(i+1)

    # print(depot_address)
    # print(city_addresses)
    # print(len(salesmen)-1)
    # print(exclusive_cities)
    # print(shared_cities)
    m = model(depot_address, city_addresses, len(salesmen)-1, exclusive_cities, shared_cities)
    
    m.get_data()


    return render(request, "result.html")