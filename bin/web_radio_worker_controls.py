import time

from base_app.multiprocess.worker import Worker
from web_radio_controls import RspGpio
from web_radio_controls import RadioEncoder

class WebRadioWorkerControls(Worker):

    def __init__(self, *args, **kwargs):
        super(WebRadioWorkerControls, self).__init__(*args, **kwargs)
        self.main_loop_sleep_time = .02
        self.msg_receiver.register_handler(
            message_type="set_encoder_max",
            message_handler=self._msg_handl_set_encoder_max)
        self.encoder_last_time = time.time()
        self.encoder_last_position = None
        self.encoder_delayed_message = None
        self.encoder_delayed_message

        # Init Raspberry Pi intrface classes
        self.rsp_gpio = RspGpio()
        self.rsp_gpio.add_input(name="btn1", gpio_num="GPIO07")
        self.rsp_gpio.add_input(name="btn2", gpio_num="GPIO15")
        self.rsp_gpio.set_inputs()
        self.rsp_enc = RadioEncoder(gpio_1="GPIO25", gpio_2="GPIO08")
        self.btn_message_type_d = {
            ("btn1", "pressed"): "btn1_pressed",
            ("btn1", "released"): "btn1_released",
            ("btn2", "pressed"): "btn2_pressed",
            ("btn2", "released"): "btn2_released",
            }

    # TODO Finish delayed message sending. Add seding delayed message after pause.
    def worker_action(self):
        btn_result = self.rsp_gpio.check_inputs()
        if btn_result:
            btn = list(btn_result.keys())[0]
            action = list(btn_result.values())[0]
            msg_type = self.btn_message_type_d[(btn, action)]
            self._send_message_to_main(msg_type=msg_type)
        enc_result = self.rsp_enc.check_inputs()
        if enc_result:
            msg_body_d = {"direction": enc_result,
                          "position": self.rsp_enc.position}
            cur_encoder_time = time.time()
            time_between_encoder_pulse = cur_encoder_time - self.encoder_last_time
            if time_between_encoder_pulse < 2:
                print("enc_time = {}".format(cur_encoder_time))
                print("time_between_encoder_pulse = {}".format(time_between_encoder_pulse))
                self.encoder_last_time = cur_encoder_time
                self.encoder_last_position = self.rsp_enc.position
                self.encoder_delayed_message = msg_body_d
            else:
                self.encoder_last_time = cur_encoder_time
                self._send_message_to_main(msg_type="encoder",
                                           msg_body=msg_body_d)
        if self.encoder_delayed_message:
            self._send_message_to_main(msg_type="encoder",
                                       msg_body=self.encoder_delayed_message)
            self.encoder_delayed_message = None
        return

    def _send_message_to_main(self, msg_type=None, msg_body=None):
        self.msg_router.send_message(
            receiving_object_name="main",
            message_type=msg_type,
            message_body=msg_body
        )
        return

    def _msg_handl_set_encoder_max(self, msg_body=None):
        self.rsp_enc.position_max = int(msg_body["position_max"])
        return
