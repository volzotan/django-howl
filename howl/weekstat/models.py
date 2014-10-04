from django.db import models

from howlcore import core

from mongodb.models import Mongodb

import json
import mongodb

from datetime import datetime, timedelta 
from django.utils.timezone import utc

import logging

logger = logging.getLogger(__name__)

MIN_LUMINOSITY = 150000
MAX_LUMINOSITY = 420000
LUMINOSITY_THRESHOLD = 100

DEVICE_TYPE = core.DeviceType.INTERFACE


class Weekstat(core.Device, core.Interface):
    db = models.ForeignKey(Mongodb)
    data = models.TextField(blank=True, null=True)

    def read(self):
        response_data = [0 for x in range(0, 6)]

        for i in range(0, 6):
            now = datetime.now()
            start = now - timedelta(days=i + 1) - timedelta(hours=now.hour) - timedelta(minutes=now.minute)
            end = start + timedelta(days=1)

            query = {"time": {"$gte": float(start.strftime('%s')), "$lt": float(end.strftime('%s'))}}
            db_data = self.db.raw_query(query)
            self.db.save()

            uncompr = []                # dont work on the mongodb cursor object directly...
            for elem in db_data:       
                uncompr.append(elem)

            for elem in uncompr:
                if (elem["luminosity"] > LUMINOSITY_THRESHOLD):
                    response_data[i] += elem["luminosity"]

            # TODO calculcate "cloudyness"-value

            response_data[i] -= MIN_LUMINOSITY
            response_data[i] /= MAX_LUMINOSITY

        response_data.reverse()
        self.data = json.dumps(response_data) # WEIRD BUG
        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()

    def ping(self):
        self.status = core.StatusType.OK
        self.save()
        logger.debug("weekstat " + self.name + " check successful")
        return True
