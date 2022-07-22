"""

coding utf-8

main.py

Nathan Hildebrand

Called from boot.py on start-up. Initiates the app.


"""

import settings

settings.do_connect()
settings.init()

import cloud_light

print('start-up complete.')

cloud_light.app()