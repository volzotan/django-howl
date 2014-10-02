from django.db import models

from django.utils.timezone import utc
import datetime
import codecs
import logging
import subprocess

from howlcore import core
from forecast.models import Forecast
from mongodb.models import Mongodb

from django.conf import settings
import os.path

logger = logging.getLogger(__name__)

DEVICE_TYPE = core.DeviceType.INTERFACE

class Inkdisplay(core.Device, core.Interface):
    forecast = models.ForeignKey(Forecast)
    db = models.ForeignKey(Mongodb)

    icons = {"clear-day", "clear-night", "rain", "snow", "sleet", "wind", "fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"}

    def read(self):
        pass

    def write(self):
        self.forecast.read()

        directory = os.path.abspath(os.path.join(settings.PROJECT_ROOT, os.pardir))
        # Open SVG to process
        output = None
        try:
            output = codecs.open(os.path.join(directory, "inkdisplay/templates/inkdisplay/image-preprocess.svg"), "r", encoding='utf-8').read()
        except Exception as e:
            logger.warn("opening svg template failed", exc_info=True)
            raise Exception("opening svg template failed")

        # Insert forecast values
        output = output.replace('TODAY_TEMPMIN', str(round(self.forecast.temp_min_today,1))).replace('TOM_TEMPMIN', str(round(self.forecast.temp_min_tomorrow,1)))
        output = output.replace('TODAY_TEMPMAX',str(round(self.forecast.temp_max_today,1))).replace('TOM_TEMPMAX', str(round(self.forecast.temp_max_tomorrow,1)))

        output = output.replace('TODAY_RAINPROB', str(int(self.forecast.rainprobability_today)) + "%").replace('TOM_RAINPROB', str(int(self.forecast.rainprobability_tomorrow)) + "%")
        output = output.replace('TODAY_WINDSPEED', str(round(self.forecast.windspeed_today,1))).replace('TOM_WINDSPEED', str(round(self.forecast.windspeed_tomorrow,1)))

        output = output.replace('SUNRISE', self.forecast.sunrise.strftime("%H:%M")).replace('SUNSET', self.forecast.sunset.strftime("%H:%M"))

        # Insert days of week
        today = datetime.datetime.today().weekday()
        days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        output = output.replace('WEEKDAY_NAME',days_of_week[today][0:2].upper()).replace('DATE_NUMBER',datetime.datetime.today().strftime("%d"))

        # Insert icons
        output = output.replace('TODAY_IMG', self.forecast.icon_today)
        output = output.replace('TOM_IMG', self.forecast.icon_tomorrow)


        output = output.replace('GRAPHIMAGEPATH', '/tmp/graphs.png')

        # Write output
        try:
            codecs.open('/tmp/inkdisplay-output.svg', 'w', encoding='utf-8').write(output)
        except Exception as e:
            logger.warn("writing svg output failed")

        # Write CSV for graph

        data = self.db.read(1440)

        try:
            f = open("/tmp/plotdata.csv", "w")
            for elem in data:
                f.write(str(elem['time']) + " " + str(int(elem['luminosity'])/10) + " " + str(elem['temperature']) + " " + str(elem['humidity']) + "\n")
        except IOError as e:
            logger.warn("writing CSV file failed", exc_info=True)
        finally:
            f.close()

        if subprocess.call([os.path.join(directory, "inkdisplay/convert.sh")]) != 0:
            logger.warn("converting inkdisplay output image failed")
            raise Exception("script returned non zero exit code")

        logger.debug("inkdisplay " + self.name + " write successfull")
        self.last_active = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.status = core.StatusType.OK
        self.save()

    def ping(self):
        self.status = core.StatusType.OK
        self.save()
        logger.debug("inkdisplay " + self.name + " ping successfull")
        return True
