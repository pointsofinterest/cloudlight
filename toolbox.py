"""

coding utf-8

toolbox.py

Nathan Hildebrand

Contains helper functions for getting weather data and setting LEDs.

"""

import settings
from machine import Pin,PWM
import math
import socket, json, io
import pickle
import time

"""Weather/LED Functions"""

def start_leds():
    print('starting leds...')

    r = Pin(4,Pin.OUT)
    g = Pin(0,Pin.OUT)
    b = Pin(5,Pin.OUT)
    r = PWM(r)
    g = PWM(g)
    b = PWM(b)

    cie = _pickle_data('read','cie')

    settings.leds = (r,g,b)
    for k in settings.leds:
        k.duty(cie[125])
    r.freq(1000)

def set_leds():
    get_weather()
    forecast = forecast()
    set_colour(_get_rgb(forecast[0]))
    set_pulse(forecast[1])
    print('cloud light updated.')

def set_colour(rgb):
    cie = _pickle_data('read','cie')

    for k in range(len(settings.leds)):
        settings.leds[k].duty(cie[rgb[k]])

# eg. set_colour((125,125,125))

def _get_rgb(forecast):
    switch = {
    0:(13,113,213),
    1:(233,150,3),
    2:(233,233,10)
    }
    return switch.get(forecast)

def forecast():
    print('checking the forecast...')
    data = _pickle_data('read','data')

    today_temp = data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]
    tomorrow_temp = data["DailyForecasts"][1]["Temperature"]["Maximum"]["Value"]
    today_precip = data["DailyForecasts"][0]["Day"]["HasPrecipitation"]
    tomorrow_precip = data["DailyForecasts"][1]["Day"]["HasPrecipitation"]

    if tomorrow_temp > (today_temp + (today_temp * 0.1)):
        # Set the light to a colour meaning tomorrow is hotter.
        fcast = 2
    elif tomorrow_temp < (today_temp - (today_temp * 0.1)):
        # Set the light to a colour meaning tomorrow is cooler.
        fcast = 0
    else:
        # Set the light to a colour meaning tomorrow is the same.
        fcast = 1

    if today_precip == True | tomorrow_precip == True:
        pulse = True
    else:
        pulse = False

    return fcast, pulse


def set_pulse(fcast):
    if fcast == True:
        orig_duty = [settings.leds[k].duty() for k in range(len(settings.leds))]

        for i in range(100):
            new_duty = []

            for k in range(len(settings.leds)):
                out = int(
                    orig_duty[k] - (math.pow(math.sin(i / 100 * math.pi),2) * orig_duty[k])
                )
                new_duty.append(out)

            settings.leds[0].duty(new_duty[0])
            settings.leds[1].duty(new_duty[1])
            settings.leds[2].duty(new_duty[2])
            del new_duty
            time.sleep_ms(5)

def check_sky(): # stub
    pass

""" HTTP/API/Data Functions """

def get_weather():
    service = 'dataservice.accuweather.com/'
    endpoint = 'forecasts/v1/daily/5day/'
    cityid = '53286'
    apikey = 'fEwAljUFRBNmVLhbRIAxYYA1AxrSmV1n'
    details = 'false'
    metric = 'true'
    url = 'http://' + service + endpoint + cityid + '?' + 'apikey=' + apikey + '&' + 'details=' + details + '&' + 'metric=' + metric
    _pickle_data('write','data',_http_get(url))

def _http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

    try:
        f = io.StringIO() # in-memory stream.
        print('retrieving weather data', end='')
        while True:
            data = s.recv(100)
            if data:
                f.write(str(data,'utf-8'))
                print('.', end='')
            else:
                print(' ')
                break
    except MemoryError as e:
        print(e)

    s.close()
    data = f.getvalue()
    f.close()
    data = json.loads(data.split('\r\n\r\n')[-1]) # Splits header and body, keeping only the body.
    return data

def _pickle_data(operation,filename,data=None):
    if operation == 'write':
        f = open(filename,'wb')
        pickle.dump(data,f)
        f.close()
        print('data saved.')
    else:
        try:
            f = open(filename,'rb')
        except OSError as e:
            print(e)
            print(filename + ' does not exist.')
        data = pickle.load(f)
        f.close()
        return data