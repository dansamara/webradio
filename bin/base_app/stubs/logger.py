from __future__ import print_function

__author__ = "Evgeny Kazanov"

import datetime
import os
import sys

DEBUG = 1
INFO = 2
WARNING = 3
ERROR = 4
CRITICAL = 5
EXCEPTION = 6


class Logger(object):
    """
    """

    def __init__(self, print_stderr=False, level=WARNING):
        self.print_stderr = print_stderr
        self.level = level
        self.level_d = {"DEBUG": DEBUG,
                        "INFO": INFO,
                        "WARNING": WARNING,
                        "ERROR": ERROR,
                        "CRITICAL": CRITICAL,
                        "EXCEPTION": EXCEPTION}

    def debug(self, msg):
        level = "DEBUG"
        self.print_msg(level, msg)
        return

    def info(self, msg):
        level = "INFO"
        self.print_msg(level, msg)
        return

    def warning(self, msg):
        level = "WARNING"
        self.print_msg(level, msg)
        return

    def error(self, msg):
        level = "ERROR"
        self.print_msg(level, msg)
        return

    def critical(self, msg):
        level = "CRITICAL"
        self.print_msg(level, msg)
        return

    def exception(self, msg):
        level = "EXCEPTION"
        self.print_msg(level, msg)
        return

    def setLevel(self, level):
        pass

    def print_msg(self, level, msg):
        # Current message level is less then self.level
        if level <= self.level:
            return
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        hostname = os.uname()[1]
        print_msg = "{} {} {} {}".format(time_str, hostname, level, msg)
        if self.print_stderr:
            sys.stderr.write(print_msg)
        else:
            print(print_msg)
        return
