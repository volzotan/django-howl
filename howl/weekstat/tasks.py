from __future__ import absolute_import

from celery import shared_task

from weekstat.models import Weekstat

@shared_task
def read(weekstatname):
    stat = Weekstat.objects.get(name=weekstatname)
    stat.read()
    stat.save()