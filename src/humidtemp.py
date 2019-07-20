"""The DHT driver is implemented in software and works on all pins:"""
from machine import Pin
import dht

dht22 = dht.DHT22(Pin(21))


def main():
    print("humidtemp.py->main()")

    dht22.measure()
    temp_c = dht22.temperature()  # eg. 23.6 (°C)
    humidity = dht22.humidity()     # eg. 41.3 (% RH)
    temp_f = temp_c * (9 / 5) + 32.0

    print('Temperature: %3.1f C' % temp_c)
    print('Temperature: %3.1f F' % temp_f)
    print('Humidity: %3.1f %%' % humidity)

    return temp_f, humidity


print('humidtemp imported')
