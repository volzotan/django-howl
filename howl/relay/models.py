from django.db import models
from howlcore import core
from django.utils.timezone import utc
import datetime
import mosquitto

import logging

DEVICE_TYPE = core.DeviceType.ACTUATOR

logger = logging.getLogger(__name__)

SWITCH_ON  = "10"
SWITCH_OFF = "01"

class Radio(core.Device, core.Interface):
    mqtt_topic = models.CharField(max_length=200)

    def write(self, data):
        client = mosquitto.Mosquitto("howl_relay")

        # self.client.on_connect = self.on_connect

        client.connect("192.168.178.55")
        if (client.publish(self.mqtt_topic, data, retain=False) != 0):
            logger.warn("publishing MQTT-msg from radio " + self.name + " failed")
            raise Exception

        client.disconnect()

        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()

    # def on_connect(self, mosq, obj, rc):
    #     if rc == 0:
    #         logger.debug("MQTT client connect successfull")

    # def check(self):
    #     # check
    #     self.is_responding = True
    #     self.save()
    #     logger.debug("radio " + self.name + " check successfull")
    #     return self.is_responding

class Relay(core.Device, core.Actuator):
    devicecode = models.CharField(max_length=10)
    radio = models.ForeignKey(Radio)

    def switch_on(self):
        self.send_to_radio(str(self.devicecode + SWITCH_ON))

    def switch_off(self):
        self.send_to_radio(str(self.devicecode + SWITCH_OFF))

    def send_to_radio(self, data):
        self.radio.write(data)

    # def check(self):
    #     self.is_responding = self.radio.check()
    #     self.save()
    #     logger.debug("relay " + self.name + " check successfull")
    #     return self.is_responding