from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from solutions.models import City, Salesman, Route

from solutions.forms import CityForm, SalesmanForm, RouteForm

# from algorithms import make_data

# Create your views here.

def top(request):
    cities = City.objects.all()
    context = {"cities": cities}
    return render(request, "solutions/top.html", context)

@login_required
def city_new(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.created_by = request.user
            city.save()
            return redirect(city_detail, city_id=city.pk)
        
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

def route_new(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("route")
    else:
        form = RouteForm()

    return render(request, "route_new.html", {'form': form})

