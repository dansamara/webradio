#import enumerate
import fileinput
import glob
import os
import re

class PlaylistIface:

    def __init__(self, playlist_dir=None):
        self.playlist_dir = playlist_dir
        self._line_re = re.compile(r'^([a-zA-Z0-9_]+)=(.*)$')
        self.playlist_d = self.read_playlists()
        self.max_station_num = len(self.playlist_d) - 1
        self.print_playlist()
        self.print_playlist_d()

    def read_playlists(self):
        pattern = os.path.join(self.playlist_dir, "*.pls")
        fname_arr = glob.glob(pattern)
        playlists_d = {}
        for cnt, fname in enumerate(fname_arr):
            entry = self.read_playlist(fname=fname)
            playlists_d[cnt] = entry
        return playlists_d

    def read_playlist(self, fname=None):
        lines_d = {}
        for line in fileinput.input([fname]):
            if line.find("=") == -1:
                continue
            line = line.rstrip("\n")
            line_obj = self._line_re.match(line)
            gr1 = line_obj.group(1)
            gr2 = line_obj.group(2)
            lines_d[gr1] = gr2
        result = {}
        result["fname"] = os.path.basename(fname)[:-4]
        if int(lines_d["NumberOfEntries"]) == 2:
            result["file"] = lines_d["File2"]
            result["title"] = lines_d["Title2"]
        elif int(lines_d["NumberOfEntries"]) == 1:
            result["file"] = lines_d["File1"]
            result["title"] = lines_d["Title1"]
        else:
            print("Do not know what to do with file: {}".format(fname))
            result["file"] = None
            result["title"] = None
        try:
            result["voice_text"] = lines_d["voice_text"]
        except KeyError:
            result["voice_text"] = result["title"]
        try:
            result["voice_lang"] = lines_d["voice_lang"]
        except KeyError:
            result["voice_lang"] = "en"
        return result

    def print_playlist(self):
        for key in self.playlist_d.keys():
            print("{} {} {}".format(key, self.playlist_d[key]["title"],self.playlist_d[key]["title"]))

    def print_playlist_d(self):
        for key, station_d in self.playlist_d.items():
            print("{}:".format(key))
            for k, v in station_d.items():
                print("\t{}: {}".format(k, v))
