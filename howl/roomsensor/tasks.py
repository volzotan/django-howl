from __future__ import absolute_import

from celery import shared_task

from roomsensor.models import Roomsensor
import time

@shared_task
def read(sensorname):
    sensor = Roomsensor.objects.get(name=sensorname)
    sensor.read()

@shared_task
def read_and_save_to_mongodb(sensorname):
    sensor = Roomsensor.objects.get(name=sensorname)
    sensor.read()

    dataset = {}
    # if (isinstance(sensor.luminosity, float) and isinstance(sensor.temperature, float) and isinstance(sensor.humidity, float)):
    dataset["luminosity"] = sensor.luminosity
    dataset["temperature"] = sensor.temperature
    dataset["humidity"] = sensor.humidity
    # else:
    #     raise Exception("write to db failed: values not from type float")

    dataset["time"] = time.time()
    sensor.db.write(dataset)