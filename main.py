# main.py

from machine import DEEPSLEEP_RESET, reset_cause

from include.secrets import _ssid, _pass
from src.ota_updater import OTAUpdater
from src.garuda import Garuda


### TODO: read these from a config file
GITHUB_REPO = 'https://github.com/desmith/Sridama_esp32_mpy'

ota = OTAUpdater(GITHUB_REPO)

VERSION = ota.get_version(directory='src', version_file_name='.version')

f = open('board.py')
BOARD = f.readline().rstrip('\n')
f.close()


def download_and_install_update_if_available():
    print('checking for updates...')
    ota.download_and_install_update_if_available(_ssid, _pass)


def start():
    print('Hare Krishna')

    carrier = Garuda(board=BOARD, version=VERSION)
    carrier.arise()


def boot():
    # check if the device woke from a deep sleep
    # (A software reset does not change the reset cause)
    if reset_cause() == DEEPSLEEP_RESET:
        print('woke from a deep sleep')

    download_and_install_update_if_available()

    while True:
        start()


boot()
