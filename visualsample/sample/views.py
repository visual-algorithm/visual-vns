from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import City, Salesman, Route
from .forms import CityForm, SalesmanForm, RouteForm
from .serializers import CitySerializer, SalesmanSerializer, RouteSerializer

# Salesmanの登録と一覧
def salesman_list(request):
    salesmen = Salesman.objects.all()
    if request.method == "POST":
        form = SalesmanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salesman_list')
    else:
        form = SalesmanForm()
    return render(request, 'salesman_list.html', {'salesmen': salesmen, 'form': form})

# Cityの登録と一覧
def city_list(request):
    cities = City.objects.all()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('city_list')
    else:
        form = CityForm()
    return render(request, 'city_list.html', {'cities': cities, 'form': form})

# Routeの登録と一覧
def route_list(request):
    routes = Route.objects.all()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm()
    return render(request, 'route_list.html', {'routes': routes, 'form': form})

class SalesmanViewSet(viewsets.ModelViewSet):
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer