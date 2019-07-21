import network
import utime
import ntptime
from machine import deepsleep, Pin
from time import sleep

from umqtt import robust as umqtt
from itertools import cycle

from src.humidtemp import main as ht
from src.icstation import readSoilMoisture
from src import water
from src.thingspeak import main as ts

from include.secrets import (AIO_CLIENT_ID,
                             AIO_SERVER,
                             AIO_PORT,
                             AIO_USER,
                             AIO_KEY,
                             AIO_FEEDS
                             )

ntptime.settime()
led = Pin(2, Pin.OUT)

### TODO: read these from a config file
# 1000 = 1 sec
# 10000 = 10 secs...
DEEPSLEEP_MIN = 1000 * 60
DEEPSLEEP_TIME = DEEPSLEEP_MIN * 10

SLEEPTIME_SEC = 60 * 20  # in seconds

AIO_FEEDS_KEYS = list(AIO_FEEDS.keys())

# deepsleep(DEEPSLEEP_TIME)
'''
Calling deepsleep() without an argument will put the device to sleep indefinitely
'''


class Garuda:
    def __init__(self, board, version):
        self.BOARD = board
        self.VERSION = version

        print('Garuda Awake!')
        print('Board: ', self.BOARD)
        print('Version: ', self.VERSION)

        (y, mo, d, h, min, s, dow, doy) = utime.localtime()
        self.timestamp = ''.join([str(y), '-', str(mo), '-', str(d),
                                  ' ',
                                  str(h), ':', str(min), ':', str(s),
                                  ' (GMT)'
                                  ])

        sta_if = network.WLAN(network.STA_IF)
        self.ipaddress = sta_if.ifconfig()[0]

    def measure(self):
        print('Garuda is fetching moisture data...')

        cnt = 0
        values = []
        voltages = []
        percentages = []
        led.value(1)
        while cnt < 6:
            cnt += 1
            sensor_value, sensor_voltage, moisture_percentage = readSoilMoisture()
            values.append(sensor_value)
            voltages.append(sensor_voltage)
            percentages.append(moisture_percentage)
            sleep(5)

        average_value = sum(values) / float(len(values))
        value = round(average_value, 2)

        average_voltage = sum(voltages) / float(len(voltages))
        voltage = round(average_voltage, 2)

        if sum(percentages) > 0:
            average_percentage = sum(percentages) / float(len(percentages))
            moisture_percentage = round(average_percentage, 2)
        else:
            moisture_percentage = 0.0

        print('\nvalue: ', value)
        print('voltage: ', voltage)
        print('moisture_percentage: ', moisture_percentage, '\n')

        if moisture_percentage < 40:
            print('opening valve...')
            water.open()
        else:
            print('closing valve...')
            water.close()

        led.value(0)

        print('Garuda is fetching temperature and humidity data...')
        temperature, humidity = ht()
        # temperature, humidity = 108.6, 45.56  $ for debugging

        self.moisture = moisture_percentage
        self.temperature = temperature
        self.humidity = humidity
        self.sensor_data = {
            'value': value,
            'percentage': moisture_percentage,
            'voltage': voltage
        }

    def sendTS(self):
        print('Garuda in flight!')
        status_msg = ' | '.join([self.timestamp,
                                 'Board: ' + self.BOARD,
                                 'Version: ' + self.VERSION,
                                 'water: ' + water.status(),
                                 'sensor_data: ' + str(self.sensor_data),
                                 'ipaddress: ' + self.ipaddress
                                 ])

        print('sending data to Thingspeak: ', status_msg)

        ts(self.moisture, self.temperature, self.humidity, status_msg)

    def sendAIO(self):
            print('Sending data to Adafruit IO...')

            # Use the MQTT protocol to connect to Adafruit IO
            client = umqtt.MQTTClient(AIO_CLIENT_ID,
                                      AIO_SERVER,
                                      AIO_PORT,
                                      AIO_USER,
                                      AIO_KEY
                                      )

            client.connect()        # Connects to Adafruit IO using MQTT
            client.check_msg()      # Action a message if one is received. Non-blocking.

            moist_sent = False
            temp_sent = False
            humi_sent = False

            toggle = cycle(AIO_FEEDS_KEYS).__next__

            while True:
                feed = toggle()

                try:

                    if feed == 'moisture':
                        client.publish(topic=AIO_FEEDS['moisture'], msg=str(self.moisture))
                        print("Moisture sent")
                        moist_sent = True

                    elif feed == 'temperature':
                        client.publish(topic=AIO_FEEDS['temperature'], msg=str(self.temperature))
                        print("Temperature sent")
                        temp_sent = True

                    elif feed == 'humidity':
                        client.publish(topic=AIO_FEEDS['humidity'], msg=str(self.humidity))
                        print("Humidity sent")
                        humi_sent = True

                except Exception as e:
                    print("Sending data to Adafruit FAILED!")
                    print(e)

                sleep(3)
                if moist_sent and temp_sent and humi_sent:
                    break

    def arise(self):
        print('Garuda Rising!')
        self.measure()

        self.sendAIO()
        # self.sendTS()

        print('feeling sleepy...')
        sleep(SLEEPTIME_SEC)
        # deepsleep(DEEPSLEEP_TIME)
        '''
        Calling deepsleep() without an argument will put the device to sleep indefinitely
        '''
