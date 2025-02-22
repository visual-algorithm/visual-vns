from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def top(request):
    return HttpResponse(b"Hello World")

def cities_new(request):
    return HttpResponse('都市セットの登録')

def cities_edit(request):
    return HttpResponse('都市セットの編集')

def cities_detail(request):
    return HttpResponse('都市セットの詳細')