import copy, uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Salesman, City, Route, Solution
from .forms import SalesmanForm, CityForm, RouteForm
from .serializers import SalesmanSerializer, CitySerializer, RouteSerializer, SolutionSerializer, UserRegistrationSerializer

from algorithms.model import model

class SalesmanViewSet(viewsets.ModelViewSet):
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [IsAuthenticated]

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def top(request):
    is_shared_exists = Salesman.objects.filter(name__contains="Shared").exists()

    if is_shared_exists == False:
        obj = Salesman(uuid=uuid.uuid4, description="Shared")
        obj.save()

    salesmen = Salesman.objects.exclude(name__contains="Shared")
    cities = City.objects.all()
    routes = Route.objects.prefetch_related("cities").select_related("depot").all()
    context = {"salesmen": salesmen, "cities": cities, "routes": routes}
    return render(request, "authsample/top.html", context)

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
        return render(request, 'authsample/city_new.html', {'form': form})

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
        return render(request, 'authsample/salesman_edit.html', {'form': form})


def salesman_detail(request, salesman_id):
    salesman = get_object_or_404(Salesman, pk=salesman_id)
    return render(request, 'authsample/salesman_detail.html', {'salesman': salesman})



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
        return render(request, 'authsample/city_new.html', {'form': form})


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
        return render(request, 'authsample/city_edit.html', {'form': form})


def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'authsample/city_detail.html', {'city': city})


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
        return render(request, "authsample/route_new.html", {'form': form})

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
        return render(request, 'authsample/route_edit.html', {'form': form})
    
def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'authsample/route_detail.html', {'route': route})

def test_detail(request, route_id):
    route = get_object_or_404(Route, uuid=route_id)
    context = {"route": route}
    return render(request, "result.html", context)



def ex_solve(request, route_id):
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

    return render(request, "authsample/result.html", context)

def send_result(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # citiesにdepotは含まれます。
    depot = route.depot
    cities = list(route.cities.all())
    salesmen = list(route.salesmen.all())

    tmp_cities = []
    for city in cities:
        if city.uuid != depot.uuid:
            tmp_cities.append(city)

    tmp_cities.insert(0, depot)
    cities = copy.deepcopy(tmp_cities)

    shared_cities = []
    exclusive_cities = [[] for i in range(len(salesmen))]
    for i in range(1, len(cities)):
        for j in range(len(salesmen)):
            if cities[i].salesman.name == salesmen[j].name:
                if salesmen[j].name == 'Shared' or salesmen[j].name == '共有':
                    shared_cities.append(i)
                else:
                    exclusive_cities[j].append(i)

    tmp_cities = [[] for i in range(len(salesmen)-1)]
    cnt = 0
    print(exclusive_cities)
    for i in range(len(exclusive_cities)):
        if len(exclusive_cities[i]):
            tmp_cities[cnt] = copy.deepcopy(exclusive_cities[i])
            cnt = cnt + 1
    
    exclusive_cities = copy.deepcopy(tmp_cities)
    
    city_addresses = []
    for city in cities:
        city_addresses.append(str(city.address))

    salesman_names = []
    for salesman in salesmen:
        salesman_names.append(str(salesman.name))

    
    print(city_addresses)
    print(salesman_names)
    print(shared_cities)
    print(exclusive_cities)
    
    m = model(route_id, len(salesmen)-1, len(cities), city_addresses, exclusive_cities, shared_cities)

    optimal_solution = m.get_data()

    optimal_path = [[] for i in range(len(salesmen)-1)]
    for i in range(len(optimal_solution)):
        for j in range(len(optimal_solution[i])):
            optimal_path[i].append(cities[optimal_solution[i][j]].name)

    html = render_to_string('authsample/'+str(route_id)+'.html')

    not_shared_list = []
    for sman in salesmen:
        if sman.name != 'Shared' and sman.name != '共有':
            not_shared_list.append(sman)

    salesman_list = [
        {
            "uuid": str(s.uuid),
            "name": s.name,
            "description": s.description,
            "created_at": s.created_at.isoformat(),
            "updated_at": s.updated_at.isoformat(),
            "created_by": s.created_by.username,
        }
        for s in not_shared_list
    ]


    return JsonResponse({
        "html": html,
        "salesmen": salesman_list,
        "pathes": optimal_path,
    })


def solve(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    # citiesにdepotは含まれます。
    depot = route.depot
    cities = list(route.cities.all())
    salesmen = list(route.salesmen.all())

    tmp_cities = []
    for city in cities:
        if city.uuid != depot.uuid:
            tmp_cities.append(city)

    tmp_cities.insert(0, depot)
    cities = copy.deepcopy(tmp_cities)

    shared_cities = []
    exclusive_cities = [[] for i in range(len(salesmen))]
    for i in range(1, len(cities)):
        for j in range(len(salesmen)):
            if cities[i].salesman.name == salesmen[j].name:
                if salesmen[j].name == 'Shared' or salesmen[j].name == '共有':
                    shared_cities.append(i)
                else:
                    exclusive_cities[j].append(i)

    tmp_cities = [[] for i in range(len(salesmen)-1)]
    cnt = 0
    print(exclusive_cities)
    for i in range(len(exclusive_cities)):
        if len(exclusive_cities[i]):
            tmp_cities[cnt] = copy.deepcopy(exclusive_cities[i])
            cnt = cnt + 1
    
    exclusive_cities = copy.deepcopy(tmp_cities)
    
    city_addresses = []
    for city in cities:
        city_addresses.append(str(city.address))

    salesman_names = []
    for salesman in salesmen:
        salesman_names.append(str(salesman.name))

    
    print(city_addresses)
    print(salesman_names)
    print(shared_cities)
    print(exclusive_cities)
    
    m = model(route_id, len(salesmen)-1, len(cities), city_addresses, exclusive_cities, shared_cities)

    optimal_solution = m.get_data()

    optimal_path = [[] for i in range(len(salesmen)-1)]
    for i in range(len(optimal_solution)):
        for j in range(len(optimal_solution[i])):
            optimal_path[i].append(cities[optimal_solution[i][j]].name)

    optimal = [[] for i in range(len(salesmen)-1)]

    for i in range(len(optimal_path)):
        for j in range(len(optimal_path[i])):
            for k in range(len(cities)):
                if cities[k].name == optimal_path[i][j]:
                    optimal[i].append(cities[k])

    not_shared_list = []
    for sman in salesmen:
        if sman.name != 'Shared' and sman.name != '共有':
            not_shared_list.append(sman)

    salesman_list = [
        {
            "uuid": str(s.uuid),
            "name": s.name,
            "description": s.description,
            "created_at": s.created_at.isoformat(),
            "updated_at": s.updated_at.isoformat(),
            "created_by": s.created_by.username,
        }
        for s in not_shared_list
    ]

    context = {
        'html_name': str(route_id)+'.html',
        'optimal': optimal,
        'salesmen': salesman_list,
    }
    #id一緒でRouteの内容だけ変更すると、html変更されないね

    return render(request, "authsample/result.html", context)


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
    # return render(request, "authsample/193ecee4-81d9-4861-a2d5-0182d010ee3a.html")
    return render(request, "authsample/result_for_ios.html", context)