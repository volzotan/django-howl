from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from roomsensor.models import Roomsensor
from roomsensor import tasks 
from howlcore import core

import logging

from mongodb.models import Mongodb
import json
import socket

logger = logging.getLogger(__name__)

def index(request):
    context = {}
    context["roomsensor_list"] = Roomsensor.objects.all()

    # for elem in context["roomsensor_list"]:
    #     try:   
    #         elem.read()
    #         elem.save()
    #     except Exception as e:
    #         logger.warn("reading roomsensor " + elem.name + " failed", exc_info=True)
    #         elem.is_responding = False
    #         elem.save()

    return render(request, 'roomsensor/overview.html', context)

def display(request, roomsensor_name):
    sensor = Roomsensor.objects.get(name=roomsensor_name)
    context = {}

    # try:   
    #     tasks.read.delay(sensor)
    # except socket.error as e:
    #     logger.warn("celery connection error, reading roomsensor " + sensor.name + " failed")
    #     context.update(core.generate_error_msg(core.MessageType.ERROR, "celery refused connection", "reading roomsensor failed"))
    #     sensor.is_responding = False
    #     sensor.save()
    # except:
    #     logger.warn("unknown error, reading roomsensor " + sensor.name + " failed", exc_info=True)
    #     context.update(core.generate_error_msg(core.MessageType.ERROR, "celery refused connection", "reading roomsensor failed"))
    #     sensor.is_responding = False
    #     sensor.save()
 
    context["roomsensor"] = sensor
    return render(request, 'roomsensor/detail.html', context)

def read(request, roomsensor_name):
    sensor = Roomsensor.objects.get(name=roomsensor_name)
    context = {}

    try:   
        sensor.read()
    except:
        logger.warn("manual read from roomsensor " + sensor.name + " failed", exc_info=True)
        context.update(core.generate_msg(core.MessageType.ERROR, "error!", "reading roomsensor failed"))

    context["roomsensor"] = sensor
    return render(request, 'roomsensor/detail.html', context)

def rawdata(request, roomsensor_name, datapoints, compression_factor):
    datapoints = int(datapoints)
    compression_factor = int(compression_factor)

    sensor = get_object_or_404(Roomsensor, name = roomsensor_name)
    mongodb = sensor.db

    datapoints = datapoints * compression_factor

    response_data = []
    db_data = mongodb.read(datapoints)

    uncompr = []                # dont work on the mongodb cursor object directly...
    for elem in db_data:        
        uncompr.append(elem)

    for i in range(0, len(uncompr)):
        if (i % compression_factor == 0): # first element
            elem = uncompr[i]
            response_data.append({"time": elem["time"], "luminosity": elem["luminosity"], "temperature": elem["temperature"], "humidity": elem["humidity"]})
        else:
            response_data[i / compression_factor]["luminosity"] += uncompr[i]["luminosity"]
            response_data[i / compression_factor]["temperature"] += uncompr[i]["temperature"]
            response_data[i / compression_factor]["humidity"] += uncompr[i]["humidity"]

        if (i % compression_factor == compression_factor - 1):
            response_data[i / compression_factor]["luminosity"] /= compression_factor
            response_data[i / compression_factor]["temperature"] /= compression_factor
            response_data[i / compression_factor]["humidity"] /= compression_factor

    # db_data = [x[1] for x in enumerate(db_data) if x[0] % 2 == 0] # discard every second element
    # for elem in db_data:
    #     response_data.append({"time": elem["time"]*1000, "luminosity": elem["luminosity"], "temperature": elem["temperature"], "humidity": elem["humidity"]})

    return HttpResponse(json.dumps(response_data), content_type="application/json")
