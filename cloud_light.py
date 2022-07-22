"""

coding utf-8

cloud_light.py

Nathan Hildebrand

Main app controlling the cloud light.


"""

import machine
import utime
import gc
import toolbox
import settings

def app():
	print('running cloud light...')

	toolbox.start_leds()
	utime.sleep(1)
	toolbox.set_leds()

	gc.collect()

	while True:

		print('sleeping...')
		utime.sleep(10800)

		# Reboot if wifi connection is lost.
		if not settings.wifi.isconnected():
			machine.reset()

		toolbox.get_weather()
		toolbox.set_leds()

		gc.collect()