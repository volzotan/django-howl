from django.db import models
from django.apps import apps
from django.utils.timezone import utc
from django.utils.timezone import localtime

def device(request):

    context = dict()

    context["apps"] = []

    for app_config in apps.get_app_configs():
        if not "django." in app_config.name: # filter out djangos own apps
            if not app_config.name == "howlcore":
                context["apps"].append(app_config)

    # app
    #   name : roomsensor
    #   verbose_name : Roomsensor

    context["howlstatus"] = "howlstatus-warn" # default / ok / warn / error

    return context