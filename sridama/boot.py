# boot.py

import network
from include.secrets import _ssid, _pass

#wlan = network.WLAN() # get current object, without changing the mode
ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)

# disable the access-point interface
ap_if.active(False)

if not sta_if.isconnected():
    print('connecting to network...')
    # activate the station interface:
    sta_if.active(True)
    sta_if.connect(_ssid, _pass)
    while not sta_if.isconnected():
        pass

print('network config:', sta_if.ifconfig())
