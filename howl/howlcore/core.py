from django.db import models
from django.conf import settings

from django.core.exceptions import ValidationError

from .models import Group

from django.db.models import get_apps
from django.apps import apps

import os
import json
import logging

logger = logging.getLogger(__name__)

APP_NAME_EXCLUSION_LIST = ["howlcore", "djcelery"]

def init():

    # logging
    module_dir = os.path.dirname(__file__)  # get current directory
    if settings.DEBUG:
        file_path = os.path.join(module_dir, '../logging_local.json')
    else:
        file_path = os.path.join(module_dir, '../logging.json')
    config = json.load(open(file_path, 'r'))
    logging.config.dictConfig(config)

    logger.info("logging initialized")

def get_apps():
    applist = []

    for app_config in apps.get_app_configs():
        if not "django." in app_config.name: # filter out djangos own apps
            if app_config.name not in APP_NAME_EXCLUSION_LIST:
                applist.append(app_config)

    return applist


def get_devices():

    devicelist = []

    for app_config in get_apps():
        for model in app_config.get_models():
            if issubclass(model, Device):
                devicelist.append(model)

    return devicelist


def generate_msg(error_type, heading, message):
    dictionary = {}
    dictionary["messages"] = [{"type": error_type, "heading": heading, "content": message}]
    return dictionary


def validate_whitespace(value):
    if value.find(" ") > 0:
        raise ValidationError("name contains whitespace")

def ping_all_devices():
    devicelist = []

    for model in get_devices():
        devicelist.extend(model.objects.all())

    for elem in devicelist:
        elem.ping()

"""

Classes

"""

class StatusType:
    UNDEFINED       = 0
    OK              = 1
    NOT_RESPONDING  = 2
    ERROR           = 3


class DeviceType:
    SENSOR      = 1
    ACTUATOR    = 2
    INTERFACE   = 3


class MessageType:
    ERROR       = "danger"
    WARN        = "warning"
    INFO        = "info"
    SUCCESS     = "success"


class Device(models.Model):
    name = models.CharField(max_length=200, validators=[validate_whitespace])
    last_active = models.DateTimeField(blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)

    STATUS_TYPE = (
        (StatusType.UNDEFINED, 'undefined'),
        (StatusType.OK, 'ok'),
        (StatusType.NOT_RESPONDING, 'not responding'),
        (StatusType.ERROR, 'error'),
    )

    status = models.IntegerField(choices=STATUS_TYPE, default=StatusType.UNDEFINED)

    class Meta:
        abstract = True

    def ping(self):
        return StatusType.UNDEFINED

    def __unicode__(self):
        return self.name


class Sensor(object):
    data = []

    def read(self):
        pass


class Actuator(object):
    def init(self):
        pass


class Interface(object):
    resources = dict()

    def read(self):
        pass

    def write(self):
        pass