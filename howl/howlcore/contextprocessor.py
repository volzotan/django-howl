from django.db import models
from django.apps import apps
from django.utils.timezone import utc
from django.utils.timezone import localtime

from howlcore import core

def device(request):

    context = dict()

    context["apps"] = []

    for app in core.get_apps():
        if not app.name == "howlcore":
            context["apps"].append(app)

    # app
    #   name : roomsensor
    #   verbose_name : Roomsensor

    context["howlstatus"] = "howlstatus-warn" # default / ok / warn / error

    return context