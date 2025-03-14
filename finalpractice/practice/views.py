from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Route, City, Salesman
from .forms import CityForm, SalesmanForm, RouteForm
from .serializers import RouteSerializer, CitySerializer, SalesmanSerializer

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

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


def top(request):
    cities = City.objects.all()
    routes = Route.objects.prefetch_related("cities").select_related("depot").all()
    context = {"cities": cities, "routes": routes}
    return render(request, "practice/top.html", context)

@login_required
def city_new(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.created_by = request.user
            city.save()
            return redirect('city_detail', city_id=city.pk)        
    else:
        form = CityForm()
        return render(request, 'practice/city_new.html', {'form': form})


@login_required
def city_edit(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    if city.created_by_id != request.user.id:
        return HttpResponseForbidden("この都市の編集は許可されていません。")
    
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('city_detail', city_id = city_id)
    else:
        form = CityForm(instance=city)
        return render(request, 'practice/city_edit.html', {'form': form})


def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'practice/city_detail.html', {'city': city})


@login_required
def route_new(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.created_by = request.user
            route.save()
            form.save_m2m()
            return redirect('route_detail', route_id=route.pk)
    else:
        form = RouteForm()
        return render(request, "practice/route_new.html", {'form': form})

@login_required
def route_edit(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    if route.created_by_id != request.user.id:
        return HttpResponseForbidden("この経路の編集は許可されていません。")

    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('route_detail', route_id = route_id)
    else:
        form = RouteForm(instance=route)
        return render(request, 'practice/route_edit.html', {'form': form})
    
def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'practice/route_detail.html', {'route': route})

def test_detail(request, route_id):
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


    return render(request, "practice/result.html")