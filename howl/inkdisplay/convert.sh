#!/bin/sh

#Path is WSGI Path (/var/www)
gnuplot /var/python/django-howl/howl/inkdisplay/generatepng.gnuplot
inkscape -f /tmp/inkdisplay-output.svg -e /tmp/inkdisplay-output-tmp.png
pngcrush -c 0 /tmp/inkdisplay-output-tmp.png /tmp/inkdisplay-output.png