from django.http import HttpResponse
from django.shortcuts import render

import logging

from inkdisplay.models import Inkdisplay
from howlcore import core

from django.core.servers.basehttp import FileWrapper

logger = logging.getLogger(__name__)

def index(request):
    return display(request, 'default')

def display(request, inkdisplay_name):
    # try: 
    inkd = Inkdisplay.objects.all()[0]

    try:
        inkd.write()
    except Exception as e:
        logger.warn("writing inkdisplay failed", exc_info=True)
        return None

    #inkd.save()
    # except Exception as e:
    #     context = {}
    #     context.update(core.generate_error_msg('danger', 'error', 'no inkdisplay found in DB'))
    #     raise
    #     return render(request, 'misc/error.html', context)

    response = HttpResponse(FileWrapper(open('/tmp/inkdisplay-output.png', 'r')), content_type='image/png')
    #response['Content-Disposition'] = 'attachment; filename=inkdisplay-output.png'

    return response     