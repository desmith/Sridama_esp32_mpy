# main.py

from machine import DEEPSLEEP_RESET, reset_cause

from include.secrets import _ssid, _pass
from src.garuda import Garuda


f = open('board.py')
BOARD = f.readline().rstrip('\n')
f.close()

f = open('version.py')
VERSION = f.readline().rstrip('\n')
f.close()

def start():
    print('Hare Krishna')

    carrier = Garuda(board=BOARD, version=VERSION)
    carrier.arise()


def boot():
    # check if the device woke from a deep sleep
    # (A software reset does not change the reset cause)
    if reset_cause() == DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    while True:
        start()


boot()
