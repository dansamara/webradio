import os

from debug_print import DebugPrint

class DeviceMpd:

    def __init__(self, mpc_cmd=None, playlist_iface=None):
        self.mpc_cmd = mpc_cmd
        self.debug_print = DebugPrint()
        self.playlist_iface = playlist_iface
        self.cur_playlist_num = None
        
    def _send_cmd_to_mpd(self, cmd=None, args=None):
        """
        Args:
            cmd: Command to send to mpd.
            args{list}: Command arguments.
        """
        command = "{} {} ".format(self.mpc_cmd, cmd)
        if args is not None:
            for arg in args:
                command += "{} ".format(arg)
        command += ">/dev/null"
        os.system(command)

    def stop(self):
        self._send_cmd_to_mpd(cmd="stop")

    def toggle(self):
        self._send_cmd_to_mpd(cmd="toggle")

    def _play_url(self, url=None):
        self.debug_print.print_msg("play_url()")
        self._send_cmd_to_mpd(cmd="clear")
        self._send_cmd_to_mpd(cmd="add", args=[url])
        self._send_cmd_to_mpd("play", args=["1"])

    def play_file(self, fname=None):
        print("play_file()")
        print("fname = {}".format(fname))
        mpd_uri = 'file://' + fname
        print("mpd_uri = {}".format(mpd_uri))
        self._send_cmd_to_mpd(cmd="clear")
        # mpc insert
        self._send_cmd_to_mpd(cmd="insert", args=["--wait", mpd_uri])
        # mpc next
        self._send_cmd_to_mpd(cmd="play")
        
    def switch_radiostation(self, playlist_num=None):
        # print("playlist_num = {}".format(playlist_num))
        url = self.playlist_iface.playlist_d[playlist_num]["file"]
        title = self.playlist_iface.playlist_d[playlist_num]["title"]
        # print("url = {}".format(url))
        print("Play: {}\t{}".format(playlist_num, title))
        self._play_url(url=url)
        self.cur_playlist_num = playlist_num
        
if __name__ == "__main__":
    import time

    MPC_CMD = "/usr/bin/mpc "
    device_mpd = DeviceMpd(mpc_cmd=MPC_CMD)
    device_mpd.stop()
    time.sleep(2)
    device_mpd.toggle()
