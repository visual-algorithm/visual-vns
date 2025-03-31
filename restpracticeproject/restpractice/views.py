import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from .models import City, Salesman, Route, Solution
from .forms import SalesmanForm, CityForm, RouteForm
from .serializers import CitySerializer, SalesmanSerializer, RouteSerializer, SolutionSerializer

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

class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [AllowAny]

def top(request):
    is_shared_exists = Salesman.objects.filter(name__contains="Shared").exists()

    if is_shared_exists == False:
        obj = Salesman(uuid=uuid.uuid4, description="Shared")
        obj.save()

    salesmen = Salesman.objects.exclude(name__contains="Shared")
    cities = City.objects.all()
    routes = Route.objects.prefetch_related("cities").select_related("depot").all()
    context = {"salesmen": salesmen, "cities": cities, "routes": routes}
    return render(request, "restpractice/top.html", context)

@login_required
def salesman_new(request):
    if request.method == 'POST':
        form = SalesmanForm(request.POST)
        if form.is_valid():
            salesman = form.save(commit=False)
            salesman.created_by = request.user
            salesman.save()
            return redirect('city_detail', salesman_id=salesman.pk)        
    else:
        form = SalesmanForm()
        return render(request, 'restpractice/city_new.html', {'form': form})

@login_required
def salesman_edit(request, salesman_id):
    salesman = get_object_or_404(Salesman, pk=salesman_id)
    # if city.created_by_id != request.user.id:
    #     return HttpResponseForbidden("この都市の編集は許可されていません。")
    
    if request.method == 'POST':
        form = CityForm(request.POST, instance=salesman)
        if form.is_valid():
            form.save()
            return redirect('salesman_detail', salesman_id = salesman_id)
    else:
        form = SalesmanForm(instance=salesman)
        return render(request, 'restpractice/salesman_edit.html', {'form': form})


def salesman_detail(request, salesman_id):
    salesman = get_object_or_404(Salesman, pk=salesman_id)
    return render(request, 'restpractice/salesman_detail.html', {'salesman': salesman})



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
        return render(request, 'restpractice/city_new.html', {'form': form})


@login_required
def city_edit(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    # if city.created_by_id != request.user.id:
    #     return HttpResponseForbidden("この都市の編集は許可されていません。")
    
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('city_detail', city_id = city_id)
    else:
        form = CityForm(instance=city)
        return render(request, 'restpractice/city_edit.html', {'form': form})


def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'restpractice/city_detail.html', {'city': city})


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
        return render(request, "restpractice/route_new.html", {'form': form})

@login_required
def route_edit(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # if route.created_by_id != request.user.id:
    #     return HttpResponseForbidden("この経路の編集は許可されていません。")

    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('route_detail', route_id = route_id)
    else:
        form = RouteForm(instance=route)
        return render(request, 'restpractice/route_edit.html', {'form': form})
    
def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'restpractice/route_detail.html', {'route': route})

def test_detail(request, route_id):
    route = get_object_or_404(Route, uuid=route_id)
    context = {"route": route}
    return render(request, "result.html", context)



def solve(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # citiesにdepotは含まれます。
    depot = route.depot
    cities = list(route.cities.all())
    salesmen = list(route.salesmen.all())
    salesman_names = []
    city_names = []
    for city in cities:
        salesman_name = city.salesman.name
        city_name = city.name
        salesman_names.append(str(salesman_name))
        city_names.append(str(city_name))

    depot_address = depot.address
    city_addresses = list(route.cities.values_list("address", flat=True))

    delete_index = 0
    for i in range(len(city_addresses)):
        if city_addresses[i] == depot_address:
            delete_index = i

    del salesman_names[delete_index]
    del city_addresses[delete_index]
    del city_names[delete_index]
    
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

    # for i in range(len(salesman_names)):
    #     if salesman_names[i] == 'shared' or salesman_names[i] == 'Shared':
    #         if i != 0:
    #             shared_cities.append(i)
    #     else:
    #         for j in range(len(salesman_name_list)):
    #             if salesman_names[i] == salesman_name_list[j]:
    #                 exclusive_cities[j].append(i)

    city_addresses.insert(0, depot_address)
    salesman_names.insert(0, 'Shared')
    city_names.insert(0, depot.name)

    # print(depot_address)
    # print(city_addresses)
    # print(len(salesmen)-1)
    # print(exclusive_cities)
    # print(shared_cities)

    m = model(route_id, len(salesmen)-1, len(cities), city_addresses, exclusive_cities, shared_cities)

    optimal_solution = m.get_data()

    optimal_path = [[] for i in range(len(salesmen)-1)]

    optimal = [[] for i in range(len(salesmen)-1)]

    for i in range(len(optimal_solution)):
        for j in range(len(optimal_solution[i])):
            optimal_path[i].append(city_names[optimal_solution[i][j]])

    for i in range(len(optimal_path)):
        for j in range(len(optimal_path[i])):
            for k in range(len(cities)):
                if cities[k].name == optimal_path[i][j]:
                    optimal[i].append(cities[k])

    try: 
        obj = Solution.objects.get(uuid=route_id)
        obj.name = route.name
        obj.ans = optimal_solution
        obj.path = optimal_path
        obj.save()
    except Solution.DoesNotExist:
        res = Solution(uuid=route_id, name=route.name, ans=optimal_solution, path=optimal_path)
        res.save()

    context = {
        'html_name': str(route_id)+'.html',
        'optimal': optimal,
        'salesmen': salesman_name_list,
    }
    #id一緒でRouteの内容だけ変更すると、html変更されないね

    return render(request, "restpractice/result.html", context)

def send_result_for_ios(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # citiesにdepotは含まれます。
    cities = list(route.cities.all())
    salesmen = list(route.salesmen.all())
    salesman_names = []
    city_names = []
    for city in cities:
        salesman_name = city.salesman.name
        city_name = city.name
        salesman_names.append(str(salesman_name))
        city_names.append(str(city_name))

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

    optimal_solution = m.get_data()

    optimal_path = [[] for i in range(len(salesmen))]
    
    for i in range(len(optimal_solution)):
        for j in range(len(optimal_solution[i])):
            optimal_path[i].append(city_names[optimal_solution[i][j]])

    try: 
        obj = Solution.objects.get(uuid=route_id)
        obj.name = route.name
        obj.ans = optimal_solution
        obj.path = optimal_path
        obj.save()
    except Solution.DoesNotExist:
        res = Solution(uuid=route_id, name=route.name, ans=optimal_solution, path=optimal_path)
        res.save()

    context = {
        'html_name': str(route_id)+'.html',
        'salesmen_name': salesman_names,
    }
    return render(request, "restpractice/result_for_ios.html", context)