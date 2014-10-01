from django.shortcuts import render
from django.db.models import get_apps
from django.apps import apps

from howlcore import core
import logging

from celery.task.control import inspect

logger = logging.getLogger(__name__)

def inject_models_in_context():

    context = {}

    context["modellist"] = []

    """

    devices = Relay    = Radio      = radio_main
                                    = radio_sec
                       = Relay      = relay_main
                                    = relay_sec
            = MongoDB  = Mongodb    = main

    """

    for app_config in apps.get_app_configs():
        if not "django." in app_config.name:  # filter out djangos own apps

            lh = {} # list helper
            lh["obj"] = app_config
            lh["children"] = []

            for model in app_config.get_models():

                lhc = {}
                lhc["obj"] = model
                lhc["modelname"] = model.__name__
                lhc["is_device"] = issubclass(model, core.Device)
                lhc["children"] = model.objects.all()

                lh["children"].append(lhc)

            context["modellist"].append(lh)

    return context


def index(request):
    context = {}  # inject_models_in_context()

    context["models"] = {}

    for app_config in apps.get_app_configs():
        if not "django." in app_config.name:  # filter out djangos own apps
            context["models"][app_config.name] = {}
            for model in app_config.get_models():

                context["models"][app_config.name][model.__name__] = model.objects.all()


    return render(request, "howlcore/overview.html", context)


def display(request):  # settings
    context = inject_models_in_context()

    return render(request, "howlcore/settings.html", context)


def logging(request):

    return None


def celery(request):
    context = {}

    try:
        i = inspect()

        temp_list = []

        for elem in i.scheduled().items()[0][1]:
            if "celery" not in str(elem):  # TODO: doesnt work
                temp_list.append(elem)

        context["celery_scheduled"] = temp_list
        context["celery_active"] = i.active().items()[0][1]
        context["celery_registered"] = i.registered().items()[0][1]
    except Exception as e:
        logger.error("celery error", exc_info=True)
        context.update(core.generate_msg(core.MessageType.ERROR, "error", "celery error"))

    return render(request, "howlcore/celery.html", context)

