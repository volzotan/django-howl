from django.db import models
from django.contrib import admin
import httplib
import json
import logging
import datetime
from django.utils.timezone import utc

from howlcore import core
from howlcore.exceptions import SensorReadError
from mongodb.models import Mongodb

DEVICE_TYPE = core.DeviceType.SENSOR

logger = logging.getLogger(__name__)

class Roomsensor(core.Device, core.Sensor):
    data = ["luminosity", "temperature", "humidity"]

    ip_address = models.GenericIPAddressField()
    url = models.CharField(max_length=200)  # '/sensorData'
    db = models.ForeignKey(Mongodb)

    luminosity = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)

    def read(self):
        conn = httplib.HTTPConnection(self.ip_address)
        try:
            conn.request("GET", self.url)
            response = conn.getresponse()
            if (response.status != 200):
                logger.error("roomsensor read failed: " + str(response.status) + " (" + response.reason + ")" )
                raise SensorReadError({response.status, response.reason})
            else:
                body = response.read()
                payload = json.loads(body)
                
                self.luminosity = int(payload["luminosity"])
                self.temperature = float(payload["temperature"])
                self.humidity = float(payload["humidity"])

                self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
                self.status = core.StatusType.OK
                self.save()
        except SensorReadError as e:
            logger.error("roomsensor " + self.name + " read failed", exc_info=True)
            self.status = core.StatusType.ERROR
            self.save()
            raise
        except Exception as e:
            logger.error("roomsensor " + self.name + " read failed", exc_info=True)
            self.status = core.StatusType.NOT_RESPONDING
            self.save()
            raise SensorReadError(e)


    def ping(self):
        try:
            conn = httplib.HTTPConnection(self.ip_address)
            conn.request("GET", self.url)
            response = conn.getresponse()
            if (response.status != 200):
                logger.error("roomsensor ping failed: " + str(response.status) + " (" + response.reason + ")")
                raise SensorReadError({response.status, response.reason})
            else:
                logger.debug("roomsensor {0} ping ok".format(self.name))
                self.status = core.StatusType.OK
        except SensorReadError:
            logger.error("roomsensor {0} ping failed".format(self.name), exc_info=True)
            self.status = core.StatusType.ERROR
        except:
            logger.error("roomsensor {0} ping failed".format(self.name), exc_info=True)
            self.status = core.StatusType.NOT_RESPONDING
        finally:
            self.save()
            return self.status