#!/usr/bin/env zsh

# latest binaries: https://micropython.org/download
mpy_binary=./bin/esp32-20190717-v1.11-163.bin
port=/dev/cu.SLAB_USBtoUART
chipset=esp32


if [ "$1" = "erase" ]; then
    echo "erasing device..."
    esptool.py --chip $chipset --port $port erase_flash

elif [ "$1" = "flash" ]; then
    echo "flashing device with micropython version: $mpy_binary..."
    esptool.py --chip $chipset --port $port --baud 460800 write_flash -z 0x1000 $mpy_binary

else
    echo "copying src to device..."
    ampy --port $port put src

fi
