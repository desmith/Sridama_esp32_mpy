from thingspeak import Channel
from include.secrets import THINGSPEAK_WRITE_KEYS


channel_esp32 = 'Sudhama'
channel_esp32_D = 'Sridama'
channel_esp32_P = 'Gauranga'
active_channel = channel_esp32

field_moisture = 'Moisture'
field_temperature = 'Temperature'
field_humidity = 'Humidity'


channels = [
    Channel(channel_esp32, THINGSPEAK_WRITE_KEYS[channel_esp32],
            [
            field_moisture,
            field_temperature,
            field_humidity
            ]
            ),
    Channel(channel_esp32_D, THINGSPEAK_WRITE_KEYS[channel_esp32_D],
            [
            field_moisture,
            field_temperature,
            field_humidity
            ]
            ),
    Channel(channel_esp32_P, THINGSPEAK_WRITE_KEYS[channel_esp32_P],
            [
            field_moisture,
            field_temperature,
            field_humidity
            ]
            )

]
