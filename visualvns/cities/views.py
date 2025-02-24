from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from cities.models import City

# Create your views here.

def top(request):
    cities = City.objects.all()
    context = {"cities": cities}
    return render(request, "cities/top.html", context)

def city_new(request):
    return HttpResponse('都市セットの登録')

def city_edit(request):
    return HttpResponse('都市セットの編集')

def city_detail(request, city_id):
    city = get_object_or_404(City, pk=city_id)
    return render(request, 'cities/city_detail.html', {'city': city})