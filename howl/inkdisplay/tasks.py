from __future__ import absolute_import

from celery import shared_task

from inkdisplay.models import Inkdisplay

@shared_task
def render_image(inkdisplay_name):
    inkd = Inkdisplay.objects.get(name=inkdisplay_name)
    inkd.read()
    inkd.save()
