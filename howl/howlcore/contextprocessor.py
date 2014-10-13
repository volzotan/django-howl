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

    howlstatus = core.StatusType.UNDEFINED

    for device in core.get_devices():
        for inst in device.objects.all():
            if inst.status > howlstatus:
                howlstatus = inst.status

    if howlstatus == core.StatusType.UNDEFINED:
        howlstatus = "default"
    elif howlstatus == core.StatusType.OK:
        howlstatus = "ok"
    elif howlstatus == core.StatusType.NOT_RESPONDING:
        howlstatus = "error"
    elif howlstatus == core.StatusType.ERROR:
        howlstatus = "error"
    else:
        howlstatus = "warn"


    context["howlstatus"] = "howlstatus-" + howlstatus  # default / ok / warn / error

    return context