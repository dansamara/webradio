import os
import sys
import subprocess

class VoiceIface:

    def __init__(self, cache_dir=None, device_mpd=None, volume=220):
        self.cache_dir = cache_dir
        self.device_mpd = device_mpd
        self.volume = volume

    def say_msg(self, msg_text=None, msg_lang=None, fname=None):
        # print("VoiceIface.say_msg()")
        # print("msg_text = {}".format(msg_text))
        # print("msg_lang = {}".format(msg_lang))
        cache_fname = os.path.join(self.cache_dir, fname + '.mp3')
        # print("cache_fname = {}".format(cache_fname))
        if not os.path.exists(cache_fname):
            self.write_to_cache(msg_text=msg_text,
                                msg_lang=msg_lang,
                                cache_fname=cache_fname)
        cmd = "amixer set Master {} 2>&1 > /dev/null".format(self.volume + 20)
        os.system(cmd)
        cmd = "mpg123 {}".format(cache_fname)
        os.system(cmd)
        cmd = "amixer set Master {} 2>&1 > /dev/null".format(self.volume)
        os.system(cmd)

    # def say_msg(self, msg_text=None, msg_lang=None, fname=None):
    #     print("VoiceIface.say_msg()")
    #     print("msg_text = {}".format(msg_text))
    #     print("msg_lang = {}".format(msg_lang))
    #     cache_fname = os.path.join(self.cache_dir, fname + '.mp3')
    #     if not os.path.exists(cache_fname):
    #         self.write_to_cache(msg_text=msg_text,
    #                             msg_lang=msg_lang,
    #                             cache_fname=cache_fname)
    #     self.device_mpd.play_file(fname=cache_fname)
        
        
    def write_to_cache(self, msg_text=None, msg_lang=None, cache_fname=None):
        # print("VoiceIface.write_to_cache()")
        cmd = "IFS=+;curl 'http://translate.google.com/translate_tts?ie=UTF-8"\
            "&q={}&tl={}&client=tw-ob'"\
            " -H 'Referer: http://translate.google.com/'"\
            " -H 'User-Agent: stagefright/1.2 (Linux;Android 5.0)' > {}".format(
            msg_text, msg_lang, cache_fname)
        print("cmd={}".format(cmd))
        os.system(cmd)
