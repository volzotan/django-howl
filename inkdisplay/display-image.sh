#!/bin/sh

HOST=192.168.178.55

cd /mnt/us/inkdisplay
rm inkdisplay-output.png

if wget -O inkdisplay-output.png http://$HOST/inkdisplay/; then
    eips -c
	eips -g inkdisplay-output.png
else
    eips -c
	eips -g inkdisplay-error.png
fi
