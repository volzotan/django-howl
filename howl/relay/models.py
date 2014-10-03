from django.db import models
from howlcore import core
from django.utils.timezone import utc
from howlcore.exceptions import CommunicationErrorException
import datetime

import socket

import logging

DEVICE_TYPE = core.DeviceType.ACTUATOR

logger = logging.getLogger(__name__)

SWITCH_ON  = "10"
SWITCH_OFF = "01"

class Radio(core.Device, core.Interface):
    ip_address = models.GenericIPAddressField()

    PORT = 8282
    TIMEOUT = 1  # seconds
    DELIMITER = "\r\n"

    CMD_PREFIX = "SEND "

    def write(self, data):

        sock = socket.socket()
        sock.settimeout(self.TIMEOUT)

        try:
            sock.connect((self.ip_address, self.PORT))
        except Exception as e:
            logger.warn("error connecting socket")
            sock.close()
            self.status = core.StatusType.NOT_RESPONDING
            self.save()
            raise CommunicationErrorException("error connecting socket")

        raw_data = self.CMD_PREFIX + data + self.DELIMITER

        sock.send(raw_data)
        logger.debug("send: " + repr(raw_data))

        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()

    def ping(self):
        # self.is_responding = self.radio.check()
        # self.save()
        # logger.debug("relay " + self.name + " ping successfull")
        # return self.is_responding
        pass

class Relay(core.Device, core.Actuator):
    devicecode = models.CharField(max_length=10)
    radio = models.ForeignKey(Radio)

    def switch_on(self):
        self.send_to_radio(str(self.devicecode + SWITCH_ON))

    def switch_off(self):
        self.send_to_radio(str(self.devicecode + SWITCH_OFF))

    def send_to_radio(self, data):
        self.radio.write(data)