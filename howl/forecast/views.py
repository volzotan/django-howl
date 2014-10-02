from django.shortcuts import render

from forecast.models import Forecast
from howlcore import core

def index(request):

    context = {}

    try: 
        forecast = Forecast.objects.all()[0]
    except Exception as e:
        context.update(core.generate_msg('danger', 'error', 'no forecast module found in DB'))
        return render(request, 'misc/error.html', context)

    try: 
        forecast.read()
    except Exception as e:
        context.update(core.generate_msg('danger', 'error', 'forecast read failed'))
        return render(request, 'misc/error.html', context)

    context["forecast"] = forecast
        
    return render(request, 'forecast/detail.html', context)