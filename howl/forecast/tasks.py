from __future__ import absolute_import

from celery import shared_task

from forecast.models import Forecast

@shared_task
def read(forecast_name):
    forecast = Forecast.objects.get(name=forecast_name)
    forecast.read()
    forecast.save()
