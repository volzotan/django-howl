from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

import logging

logger = logging.getLogger(__name__)

class OPTION:
    EXISTENCE               = 0
    EQUAL                   = 1
    GREATER_THAN            = 2
    GREATER_THAN_OR_EQUAL   = 3
    LESS_THAN               = 4
    LESS_THAN_OR_EQUAL      = 5


class Rule(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    OPTION = (
        (OPTION.EXISTENCE, 'E'),
        (OPTION.EQUAL, '=='),
        (OPTION.GREATER_THAN, '>'),
        (OPTION.GREATER_THAN_OR_EQUAL, '>='),
        (OPTION.LESS_THAN, '<'),
        (OPTION.LESS_THAN_OR_EQUAL, '<='),
    )

    option = models.IntegerField(choices=OPTION)

    origin_device_type = models.ForeignKey(ContentType, related_name='rule_origin')
    origin_object_id = models.PositiveIntegerField()
    origin_device = generic.GenericForeignKey('origin_device_type', 'origin_object_id')

    origin_attribute = models.CharField(max_length=200)  # method or var
    origin_value = models.CharField(max_length=200, blank=True, null=True)

    destination_device_type = models.ForeignKey(ContentType, related_name='rule_destination')
    destination_object_id = models.PositiveIntegerField()
    destination_device = generic.GenericForeignKey('destination_device_type', 'destination_object_id')

    destination_method = models.CharField(max_length=200)  # method
    destination_value = models.CharField(max_length=200, blank=True, null=True)

    # if THIS                           then  THAT
    #    origin                               destination
    # if Sensor.Attribute OPTION Value  then  Device Method Value
    #    query on objects / room / group      query

    def run(self):
        pass

    def test(self):
        return self._eval()

    def trigger(self):
        self._execute()

    def _execute(self):
        try:
            if self.destination_value is not None and self.destination_value != "":
                result = getattr(self.destination_device, self.destination_method)(self.destination_value)
            else:
                result = getattr(self.destination_device, self.destination_method)()
        except AttributeError as e:
            logger.error("trigger: method [{0}] does not exist in {1}".format(self.destination_method, str(self.destination_device)))
            raise e

        return result

    def _eval(self):
        orig_attr = getattr(self.origin_device, self.origin_attribute)
        orig_val = self.origin_value

        if self.option == OPTION.EXISTENCE:
            if orig_attr is not None:
                return True
        elif self.option == OPTION.EQUAL:
            if orig_attr == orig_val:
                return True
        elif self.option == OPTION.GREATER_THAN:
            if orig_attr > orig_val:
                return True
        elif self.option == OPTION.GREATER_THAN_OR_EQUAL:
            if orig_attr >= orig_val:
                return True
        elif self.option == OPTION.LESS_THAN:
            if orig_attr < orig_val:
                return True
        elif self.option == OPTION.LESS_THAN_OR_EQUAL:
            if orig_attr >= orig_val:
                return True

        return False

    def __unicode__(self):
        return self.name
