from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from visualapp.models import Cource
from django.contrib.auth.decorators import login_required
from visualapp.forms import CourceForm

# Create your views here.

def top(request):
    cources = Cource.objects.all()
    context = {'cources': cources}
    return render(request, "visualapp/top.html", context)

@login_required
def cource_new(request):
    if request.method == 'POST':
        form = CourceForm(request.POST)
        if form.is_valid():
            cource = form.save(commit=False)
            cource.save()
            return redirect(cource_detail, cource_id = cource.pk)
    else:
        form = CourceForm()
    
    return render(request, "visualapp/cource_new.html",{'form': form})

@login_required
def cource_edit(request, cource_id):
    cource = get_object_or_404(Cource, pk=cource_id)
    

def cource_detail(request, cource_id):
    cource = get_object_or_404(Cource, pk=cource_id)
    return render(request, 'visualapp/cource_detail.html', {'cource':cource})