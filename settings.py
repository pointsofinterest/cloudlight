"""

coding utf-8

settings.py

Nathan Hildebrand

Start-up functions, globals, and constants.


"""

import upip
import ntptime
import utime

import network, settings

def init():
    upip.install('pickle')
    import pickle
    print('setting up cloud light...')

    global leds
    global wifi

    OFFSET = -25200
    rtc = utime.localtime(ntptime.time()+OFFSET)

    cie = (
    0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 
    4, 5, 5, 6, 6, 7, 7, 8, 8, 8, 
    9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 
    14, 15, 15, 16, 17, 17, 18, 19, 19, 20, 
    21, 22, 22, 23, 24, 25, 26, 27, 28, 29, 
    30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 
    40, 42, 43, 44, 45, 47, 48, 50, 51, 52, 
    54, 55, 57, 58, 60, 61, 63, 65, 66, 68, 
    70, 71, 73, 75, 77, 79, 81, 83, 84, 86, 
    88, 90, 93, 95, 97, 99, 101, 103, 106, 108, 
    110, 113, 115, 118, 120, 123, 125, 128, 130, 133, 
    136, 138, 141, 144, 147, 149, 152, 155, 158, 161, 
    164, 167, 171, 174, 177, 180, 183, 187, 190, 194, 
    197, 200, 204, 208, 211, 215, 218, 222, 226, 230, 
    234, 237, 241, 245, 249, 254, 258, 262, 266, 270, 
    275, 279, 283, 288, 292, 297, 301, 306, 311, 315, 
    320, 325, 330, 335, 340, 345, 350, 355, 360, 365, 
    370, 376, 381, 386, 392, 397, 403, 408, 414, 420, 
    425, 431, 437, 443, 449, 455, 461, 467, 473, 480, 
    486, 492, 499, 505, 512, 518, 525, 532, 538, 545, 
    552, 559, 566, 573, 580, 587, 594, 601, 609, 616, 
    624, 631, 639, 646, 654, 662, 669, 677, 685, 693, 
    701, 709, 717, 726, 734, 742, 751, 759, 768, 776, 
    785, 794, 802, 811, 820, 829, 838, 847, 857, 866, 
    875, 885, 894, 903, 913, 923, 932, 942, 952, 962, 
    972, 982, 992, 1002, 1013, 1023
    )

    f = open('cie','wb')
    pickle.dump(cie,f)
    f.close()

def do_connect():

    ssid = 'Woodland2'
    pwd = 'iwanttobelieve'
    settings.wifi = network.WLAN(network.STA_IF)
    settings.wifi.active(True)

    if not settings.wifi.isconnected():
        print('connecting to network...')
        settings.wifi.connect(ssid, pwd)

        while not settings.wifi.isconnected():
            pass

    print('network config:', settings.wifi.ifconfig())