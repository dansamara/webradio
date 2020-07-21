#! /usr/bin/env python3

from gpiozero import LED
from gpiozero import Button
from time import sleep

print("Start control.py")

# LED1 - Pin18   GPIO24
# LED2 - Pin16   GPIO23
# LED3 - Pin8    GPIO14
# LED4 - Input power

# BUTTON1 - Pin12  GPIO18 -> PIN26 GPIO7
# BUTTON2 - Pin10  GPIO15
# BUTTON3 - Power

# Rotary encoder
# ENC1     - Pin22  GPIO25
# ENC2     - Pin24  GPIO8

class RadioIface:

    def __init__(self):
        self.led_1 = LED("GPIO24")
        self.led_2 = LED("GPIO23")
        self.led_3 = LED("GPIO14")
        self.button_1 = Button("GPIO7")
        self.button_2 = Button("GPIO15")
        self.enc_1 = Button("GPIO25")
        self.enc_2 = Button("GPIO08")

    def all_leds_on(self):
        self.led_1.on()
        self.led_2.on()
        self.led_3.on()
        return

    def all_leds_off(self):
        self.led_1.off()
        self.led_2.off()
        self.led_3.off()
        return

    def print_buttons(self):
        # print("-------------------------------------------------")
        print("b1={} b2={} enc1={} enc2={}".format(self.button_1.is_pressed, self.button_2.is_pressed,
                                                   self.enc_1.is_pressed, self.enc_2.is_pressed))

    def print_encoder(self):
        sym_d = {True: "+", False: "|"}
        print("{}     {}".format(sym_d[self.enc_1.is_pressed], sym_d[self.enc_2.is_pressed]))
        return
        
radio_iface = RadioIface()


print("enc1    enc2")
while True:
    # radio_iface.all_leds_on()
    # sleep(1)
    # radio_iface.all_leds_off()
    # sleep(1)

    # radio_iface.print_buttons()

    radio_iface.print_encoder()

    
    sleep(1)

    
