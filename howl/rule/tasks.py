from __future__ import absolute_import

from celery import shared_task

from rule.models import Rule

@shared_task
def run(sensorname):
    rules = Rule.objects.all()
    for rule in rules:
        if rule.active:
            rule.run()