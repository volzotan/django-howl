from django.db import models
from django.utils.timezone import utc
import datetime
import httplib
import json
import logging

from howlcore import core
from howlcore.exceptions import SensorReadError

DEVICE_TYPE = core.DeviceType.SENSOR

logger = logging.getLogger(__name__)

class Forecast(core.Device, core.Sensor):

    location = models.CharField(max_length=100)
    api_key  = models.CharField(max_length=100)

    icon_today    = models.CharField(max_length=100, blank=True)
    icon_tomorrow = models.CharField(max_length=100, blank=True)

    temp_min_today            = models.FloatField(blank=True, default=0)
    temp_max_today            = models.FloatField(blank=True, default=0)
    temp_min_tomorrow         = models.FloatField(blank=True, default=0)
    temp_max_tomorrow         = models.FloatField(blank=True, default=0)
    humidity_today            = models.FloatField(blank=True, default=0)
    humidity_tomorrow         = models.FloatField(blank=True, default=0)
    windspeed_today           = models.FloatField(blank=True, default=0)
    windspeed_tomorrow        = models.FloatField(blank=True, default=0)
    rainprobability_today     = models.FloatField(blank=True, default=0)
    rainprobability_tomorrow  = models.FloatField(blank=True, default=0)

    sunrise                   = models.TimeField(blank=True, default=0)
    sunset                    = models.TimeField(blank=True, default=0)

    url = "api.forecast.io"
    options = "units=si"

    ICONS = {"clear-day", "clear-night", "rain", "snow", "sleet", "wind", "fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"}

    def set_icon(cls, icon):
        if icon not in cls.ICONS:
            return "default"

        return icon

    def read(self):
        query = "/forecast/" + self.api_key + "/" + self.location + "?" + self.options
        conn = httplib.HTTPSConnection(self.url)
        try:
            conn.request("GET", query)
            response = conn.getresponse()
            if (response.status != 200):
                logger.error("forecast replied with non 200 response: " + response.status + " | " + response.reason)
                raise SensorReadError({response.status, response.reason})
            else:
                self.status = core.StatusType.OK
                self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
                
                body = response.read()
                data = json.loads(body)

                today = data["daily"]["data"][1]
                tomorrow = data["daily"]["data"][2]

                self.icon_today = self.set_icon(data["currently"]["icon"])
                self.icon_tomorrow = self.set_icon(tomorrow["icon"])

                self.temp_min_today = today["temperatureMin"]
                self.temp_max_today = today["temperatureMax"]
                self.temp_min_tomorrow  = tomorrow["temperatureMin"]
                self.temp_max_tomorrow  = tomorrow["temperatureMax"]

                self.windspeed_today = data["currently"]["windSpeed"]
                self.windspeed_tomorrow = tomorrow["windSpeed"]

                self.rainprobability_today = today["precipProbability"] * 100
                self.rainprobability_tomorrow = tomorrow["precipProbability"] * 100

                self.sunrise = datetime.datetime.fromtimestamp(int(today["sunriseTime"]))
                self.sunset = datetime.datetime.fromtimestamp(int(today["sunsetTime"]))

                self.save()
        except Exception as e:
            logger.error("forecast {0} read failed".format(self.name), exc_info=True)
            self.status = core.StatusType.ERROR
            self.save()
            raise SensorReadError(e)

    # TODO: def ping(self):