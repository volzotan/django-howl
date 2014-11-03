from __future__ import absolute_import
from celery import shared_task

from howlcore import core

@shared_task
def ping_devices():
    core.ping_all_devices()
