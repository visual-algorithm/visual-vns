from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from cities.models import City

from cities.forms import CityForm

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

def city_edit(request):
    return HttpResponse('都市セットの編集')

def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'cities/city_detail.html', {'city': city})