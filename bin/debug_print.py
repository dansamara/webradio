import os

class DebugPrint:

    def __init__(self):

        try:
            os.environ["DEBUG_PRINT"]
            self.print_flag = True
        except:
            self.print_flag = False

    def print_msg(self, msg):
        if self.print_flag:
            print(msg)
        return
