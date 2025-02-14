from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from routes.models import Route
from django.contrib.auth.decorators import login_required

from routes.forms import RouteForm
# Create your views here.

def top(request):
    routes = Route.objects.all()
    context = {"routes": routes}
    return render(request, "routes/top.html", context)

@login_required
def route_new(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.created_by = request.user
            route.save()
            return redirect(route_detail, route_id = route.pk)
    else:
        form = RouteForm()
    return render(request, "routes/route_new.html", {'form': form})
        

@login_required
def route_edit(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    if route.created_by_id != request.user.id:
        return HttpResponseForbidden("このルートの編集は許可されていません。")
    
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect(route_detail, route_id = route_id)
    else:
        form = RouteForm(instance=route)
    return render(request, "routes/route_edit.html", {'form': form})
        
def route_detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, 'routes/route_detail.html', {'route': route}) 