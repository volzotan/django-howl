from django.shortcuts import render, redirect
from django.http import HttpResponse

import logging
import json

from relay.models import *

logger = logging.getLogger(__name__)

def index(request):
    context = {}
    context["relay_list"] = Relay.objects.all()
    context["radio_list"] = Radio.objects.all()
        
    return render(request, 'relay/overview.html', context)

def display(request, relay_name):
    pass

def switch(request, relay_name, switch):
    logger.debug("relay " + relay_name + " switched " + switch)

    context = {}

    # switch and check if error occured
    relay = Light.objects.get(name = relay_name)
    if (switch == "on"):
        relay.switch_on()
    else:
        if (switch == "off"):
            relay.switch_off()
        else:
            # bad request
            pass

    # context["messages"] =  [{"type":"danger","heading":"error","content":"switching relay failed"}]

    return render(request, 'misc/message.html', context)

    # response_data = {}
    # response_data['type'] = 'danger'
    # response_data['heading'] = 'error'
    # response_data['content'] = 'switching relay failed'
    # return HttpResponse(json.dumps(response_data), content_type="application/json")

    # return redirect(index)