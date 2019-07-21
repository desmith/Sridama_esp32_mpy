from machine import ADC, Pin

sensor = ADC(Pin(34))
# sensor.atten(ADC.ATTN_11DB)
# 11DB attenuation allows for a maximum input voltage
#  of approximately 3.6v (default is 0-1.0v)

SENSOR_SATURATION_LEVEL  = 3840
SENSOR_DRYNESS_LEVEL     = 4095

def readSoilMoisture():
    value = sensor.read()
    voltage = value / 1000  # convert digital value to decimal
    percentage = 100.00 * (SENSOR_DRYNESS_LEVEL - value) / SENSOR_SATURATION_LEVEL

    print('\nsensor_value: ', value)
    print('sensor_voltage: ', voltage)
    print('moisture_percentage: ', percentage)
    print('difference: ', SENSOR_DRYNESS_LEVEL - value)

    return value, voltage, percentage
