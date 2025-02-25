from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from cities.models import City, Salesman

from cities.forms import CityForm, SolveForm

from algorithms import make_data

# Create your views here.

def top(request):
    cities = City.objects.all()
    context = {"cities": cities}
    return render(request, "cities/top.html", context)

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
        return render(request, 'cities/city_new.html', {'form': form})

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
        return render(request, 'cities/city_edit.html', {'form': form})


def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'cities/city_detail.html', {'city': city})

def solve_prepare(request):
    selected_cities = []
    if request.method == "POST":
        form = SolveForm(request.POST)
        if form.is_valid():
            selected_cities = form.cleaned_data['cities']

    else:
        form = SolveForm()
    return render(request, 'cities/solve_prepare.html', {'form': form, 'selected_cities': selected_cities})

def solve(request, selected_cities):
    m = make_data.model()

    return render(request, 'cities/solve.html')