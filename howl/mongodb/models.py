from django.db import models
from django.utils.timezone import utc
import datetime
import pymongo
import json
import logging

from howlcore import core

logger = logging.getLogger(__name__)

DEVICE_TYPE = core.DeviceType.INTERFACE

class Mongodb(core.Device, core.Interface):

    attributes = ["read", "write"]

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    database_name = models.CharField(max_length=200)
    collection_name = models.CharField(max_length=200)

    document_count = models.IntegerField(blank=True, null=True)

    def init(self):
        self.connection = pymongo.Connection("mongodb://" + self.username + ":" + self.password + "@" + self.url)
        self.db = self.connection[self.database_name]
        self.collection = self.db[self.collection_name]
        self.document_count = self.collection.count()

    # def check(self):
    #     try:
    #         self.init()
    #         self.is_responding = True
    #         self.document_count = self.collection.count()
    #         self.save()
    #         logger.debug("mongodb " + self.name + " check successful")
    #         return True
    #     except Exception as e:
    #         self.is_responding = False
    #         self.save()
    #         logger.warn("mongodb " + self.name + " check failed")
    #         return False

    def read(self, count):
        self.init()
        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()
        return self.collection.find().sort("_id",pymongo.DESCENDING).limit(count)

    def raw_query(self, query):  #, **kwargs):
        self.init()
        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()
        return self.collection.find(query).sort("_id",pymongo.DESCENDING)  #.limit(count)

    def write(self, data):
        self.init()
        self.collection.insert(data)
        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()

    def ping(self):
        try:
            self.init()
            self.collection.find()
            self.status = core.StatusType.OK
            logger.debug("mongodb {0} ping ok".format(self.name))
        except Exception:
            logger.error("mongodb {0} ping failed".format(self.name), exc_info=True)
            self.status = core.StatusType.ERROR
        finally:
            self.save()
            return self.status
