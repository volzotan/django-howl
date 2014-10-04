from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from weekstat.models import Weekstat
from weekstat import tasks

def index(request):
    pass

def display(request):
    pass

def rawdata(request, weekstat_name):
    weekstat = get_object_or_404(Weekstat, name = weekstat_name)

    return HttpResponse(weekstat.data, content_type="application/json")
