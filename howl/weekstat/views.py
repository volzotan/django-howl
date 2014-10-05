from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from weekstat.models import Weekstat
from weekstat import tasks

def index(request):
    context = {}
    context["object_list"] = Weekstat.objects.all()

    return render(request, 'weekstat/overview.html', context)

def display(request, weekstat_name):
    weekstat = get_object_or_404(Weekstat, name = weekstat_name)
    weekstat.read()

    return redirect('howlcore.views.index')

def rawdata(request, weekstat_name):
    weekstat = get_object_or_404(Weekstat, name = weekstat_name)

    return HttpResponse(weekstat.data, content_type="application/json")
