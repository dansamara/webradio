#! /usr/bin/env python3


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


from gpiozero import Button
from time import sleep

class RspGpio:

    def __init__(self):
        self.inputs_d = {}
        # Format: {"<name>": {"gpio_num": "<GPIONUM>",
        #                     "state_prev": <True/False>,
        #                     "button_obj": <button_obj>}}
        self.leds_d = {}
        # Format: {"<name>": {"gpio_num": "<GPIONUM>",
        #                     "led_obj": <led_obj>}}

    def add_input(self, name=None, gpio_num=None,):
        tmp_input_d = {"gpio_num": gpio_num,
                      "state_prev": None,
                      "button_obj": Button(gpio_num)}
        self.inputs_d[name] = tmp_input_d

    def set_inputs(self):
        for name in self.inputs_d.keys():
            self.inputs_d[name]["state_prev"] = \
                self.inputs_d[name]["button_obj"].is_pressed

    def check_inputs(self):
        result = {}
        for name in self.inputs_d.keys():
            state = self.inputs_d[name]["button_obj"].is_pressed
            if state == self.inputs_d[name]["state_prev"]:
                continue
            if self.inputs_d[name]["state_prev"] and not state:
                result[name] = "pressed"
            elif not self.inputs_d[name]["state_prev"] and state:
                result[name] = "released"
            self.inputs_d[name]["state_prev"] = state
        return result

    def print_inputs(self):
        for name in self.inputs_d.keys():
            print("{} - {}".format(name, self.inputs_d[name]))

# TODO: Add self.max_value. If position is bigger then it do not change it
class RadioEncoder:

    def __init__(self, gpio_1=None, gpio_2=None ):
        self.name_1 = "enc_1"
        self.name_2 = "enc_2"
        self.rsp_gpio = RspGpio()
        self.rsp_gpio.add_input(name=self.name_1, gpio_num=gpio_1)
        self.rsp_gpio.add_input(name=self.name_2, gpio_num=gpio_2)
        self.rsp_gpio.set_inputs()
        self.enc_1_prev = self.rsp_gpio.inputs_d[self.name_1]["button_obj"]\
                                       .is_pressed
        self.enc_2_prev = self.rsp_gpio.inputs_d[self.name_2]["button_obj"]\
                                       .is_pressed
        self.enc_1_cur = None
        self.enc_2_cur = None
        self.result_table_d = {(False, False, False, True): "right",
                               (False, True, True, True): "right",
                               (True, True, True, False): "right",
                               (True, False, False, False): "right",
                               (False, False, True, False): "left",
                               (True, False, True, True): "left",
                               (True, True, False, True): "left",
                               (False, True, False, False): "left",
                               (False, False, False, False): "stop",
                               (True, True, True, True): "stop",
                               (True, False, True, False): "stop",
                               (False, True, False, True): "stop"}
        self.position = 0
        self.position_max = None

    def get_enc_state(self):
        self.enc_1_cur = self.rsp_gpio.inputs_d[self.name_1]["button_obj"]\
                                      .is_pressed
        self.enc_2_cur = self.rsp_gpio.inputs_d[self.name_2]["button_obj"]\
                                      .is_pressed
        return

    def check_inputs(self):
        enc_rotated = self.rsp_gpio.check_inputs()
        result = None
        if enc_rotated:
            self.get_enc_state()
            key = (self.enc_1_prev, self.enc_2_prev, self.enc_1_cur, self.enc_2_cur)
            try:
                result = self.result_table_d[key]
            except KeyError:
                print("except KeyError")
                print("Key before: {}".format(key_before))
                print("Key  after: {}".format(key))
                result = "stop"
            self.enc_1_prev = self.enc_1_cur
            self.enc_2_prev = self.enc_2_cur
            self.set_position(rotation_direction=result)
            return result
        return

    def set_position(self, rotation_direction=None):
        if rotation_direction == "right":
            self.position += 1
        elif rotation_direction == "left":
            self.position -= 1
        if self.position < 0:
            self.position = 0
        if self.position_max and self.position > self.position_max:
            self.position = self.position_max
        return self.position


if __name__ == "__main__":
    rsp_gpio = RspGpio()
    rsp_gpio.add_input(name="btn1", gpio_num="GPIO07")
    rsp_gpio.add_input(name="btn2", gpio_num="GPIO15")
    rsp_gpio.set_inputs()
    rsp_enc = RadioEncoder(gpio_1="GPIO25", gpio_2="GPIO08")
    while True:
        btn_result = rsp_gpio.check_inputs()
        if btn_result:
            print(btn_result)
        enc_result = rsp_enc.check_inputs()
        if enc_result:
            print("Encoder rotated: {}, position: {}".format(enc_result, rsp_enc.position))
        sleep(.02)
