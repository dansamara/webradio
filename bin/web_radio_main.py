from __future__ import print_function

__author__ = "Evgeny Kazanov"

import os
import sys
import time

from base_app.multiprocess.main import Main
from base_app.misc.timer import Timer
from web_radio_worker_controls import WebRadioWorkerControls
from web_radio_voice_iface import VoiceIface
from device_mpd import DeviceMpd
from device_mpd_playlist_iface import PlaylistIface


MPC_CMD = "/usr/bin/mpc "
BASE_DIR = os.getcwd()
PLAYLIST_DIR = os.path.join(BASE_DIR, "var/web_radiostations")
CACHE_DIR = os.path.join(BASE_DIR, "var/voice_cache")

class WebRadioMain(Main):

    def __init__(self, *args, **kwargs):
        super(WebRadioMain, self).__init__(*args, **kwargs)
        self.msg_receiver.register_handler(
            message_type="btn1_pressed",
            message_handler=self._msg_handl_btn1_pressed)
        self.msg_receiver.register_handler(
            message_type="btn1_released",
            message_handler=self._msg_handl_btn1_released)
        self.msg_receiver.register_handler(
            message_type="btn2_pressed",
            message_handler=self._msg_handl_btn2_pressed)
        self.msg_receiver.register_handler(
            message_type="btn2_released",
            message_handler=self._msg_handl_btn2_released)
        self.msg_receiver.register_handler(
            message_type="encoder",
            message_handler=self._msg_handl_enc)
        # ========================================
        self.playlist_iface = PlaylistIface(playlist_dir=PLAYLIST_DIR)
        self.device_mpd = DeviceMpd(mpc_cmd=MPC_CMD, playlist_iface=self.playlist_iface)
        self.voice_iface = VoiceIface(cache_dir=CACHE_DIR, device_mpd=self.device_mpd)
        # ========================================
        self._enc_position_max_sent_flag = False
        self.cur_playlist_num = None
        # New variables for avoid switching when the encoder switches too fast
        # The method: self._delayed_radiostation_switching()
        self.last_switching_time = None
        self.delayed_station_switching_flag = False
        self.delayed_station_playlist_num = None

    def main_action(self):
        # print("WebRadioMain.main_action()")
        if not self._enc_position_max_sent_flag:
            self._send_enc_position_max()
            self._enc_position_max_sent_flag = True
        return

    def _msg_handl_btn1_pressed(self, msg_body=None):
        print("_msg_handl_btn1_pressed()")
        print("Mute")
        self.device_mpd.stop()

    def _msg_handl_btn1_released(self, msg_body=None):
        print("_msg_handl_btn1_released()")
        print("Unmute")
        self.device_mpd.toggle()

    def _msg_handl_btn2_pressed(self, msg_body=None):
        print("_msg_handl_btn2_pressed()")
        # cur_playlist_num = self.device_mpd.cur_playlist_num
        # self.say_radiostation_name(playlist_num=cur_playlist_num)
        self.voice_iface.say_msg(msg_text="Выключаюсь", msg_lang="ru", fname="system_cmd_switch_off")
        cmd = "sudo shutdown -h now"
        os.system(cmd)

    def say_radiostation_name(self, playlist_num=None):
        if playlist_num is None:
            return
        # print("Playlist current number = {}".format(playlist_num))
        title = self.playlist_iface.playlist_d[playlist_num]["title"]
        print("title = {}".format(title))
        voice_text = self.playlist_iface.playlist_d[playlist_num]["voice_text"]
        voice_lang = self.playlist_iface.playlist_d[playlist_num]["voice_lang"]
        voice_fname = self.playlist_iface.playlist_d[playlist_num]["fname"]
        self.device_mpd.stop()
        self.voice_iface.say_msg(
            msg_text=voice_text, msg_lang=voice_lang, fname=voice_fname)
        time.sleep(2)
        self.device_mpd.switch_radiostation(playlist_num=playlist_num)

    def _msg_handl_btn2_released(self, msg_body=None):
        print("_msg_handl_btn2_released()")

    def _msg_handl_enc(self, msg_body=None):
        # print("_msg_handl_enc(), msg_body: {}".format(msg_body))
        playlist_num = int(msg_body["position"])
        self.device_mpd.switch_radiostation(playlist_num=playlist_num)
        self.say_radiostation_name(playlist_num=playlist_num)
        self.cur_playlist_num = playlist_num

    def _send_enc_position_max(self):
        message_body = {"position_max": self.playlist_iface.max_station_num}
        self.msg_router.send_message(
            receiving_object_name="worker_controls",
            message_type="set_encoder_max",
            message_body=message_body)

    def _delayed_radiostation_switching(self):
        if self.delayed_station_switching_flag:
            pass
        self.delayed_station_switching_flag = False

main = WebRadioMain()
main.main_loop_sleep_time = 0.2
worker_controls = WebRadioWorkerControls(name="worker_controls")
main.register_worker(worker=worker_controls)

main.run()

sys.exit(0)
