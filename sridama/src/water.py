from machine import Pin, Signal

valve_pin = Pin(22, Pin.OUT)
valve = Signal(valve_pin, invert=False)


def open():
    valve.off()


def close():
    valve.on()


def status():
    return 'stopped' if valve.value() else 'flowing'


close()
