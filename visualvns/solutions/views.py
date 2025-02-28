from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from solutions.models import City, Salesman, Route

from solutions.forms import CityForm, SalesmanForm, RouteForm

# from algorithms import make_data

# Create your views here.

def top(request):
    cities = City.objects.all()
    routes = Route.objects.prefetch_related("cities").select_related("depot").all()
    context = {"cities": cities, "routes": routes}
    return render(request, "solutions/top.html", context)

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
        return render(request, 'solutions/city_new.html', {'form': form})

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
        return render(request, 'solutions/city_edit.html', {'form': form})


def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'solutions/city_detail.html', {'city': city})

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
        return render(request, "solutions/route_new.html", {'form': form})

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
        return render(request, 'solutions/route_edit.html', {'form': form})
    
def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'solutions/route_detail.html', {'route': route})

def solve(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'solutions/solve.html', {"route": route})