from django.shortcuts import render

from mongodb.models import Mongodb

def index(request):
    context = {}
    context["mongodb_list"] = Mongodb.objects.all()
    return render(request, 'mongodb/overview.html', context)

def display(request, mongodb_name):
    mongodb = Mongodb.objects.get(name=mongodb_name)
    context = {}
    # mongodb.check()
    context["mongodb"] = mongodb

    return render(request, "mongodb/detail.html", context)