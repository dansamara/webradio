#! /usr/bin/env python3

from gpiozero import LED
from time import sleep

led = LED("GPIO14")

while True:
    led.on()
    sleep(1)

