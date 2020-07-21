#! /usr/bin/python3

from gpiozero import LED
from time import sleep

from subprocess import call
call(['espeak “Welcome\ to\ the\ world\ of\ Robots” 2>/dev/null'], shell=True)

