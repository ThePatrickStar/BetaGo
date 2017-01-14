import threading
import pyautogui
from screenpixel import ScreenPixel


FINGER_KEY = ['d', 'f', 'j', 'k']
lock = threading.Lock()


def deserve_click(rgb):
    if rgb[0] < 15 and rgb[1] < 15 and rgb[2] < 15:
        # or (rgb[0] > 250 and 175 < rgb[1] < 185 and rgb[2] < 8)
        return True
    else:
        return False


def deserve_stop(rgb):
    if rgb[0] > 250 and rgb[1] > 250 and rgb[2] > 250:
        return True
    else:
        return False


class Finger (threading.Thread):
    def __init__(self, sp, left_border, board_width, hand, num, baseline):
        threading.Thread.__init__(self)
        self.sp = sp
        self.left_border = left_border
        self.board_width = board_width
        self.hand = hand
        self.num = num
        self.baseline = baseline

    def run(self):
        while True:
            if self.hand.stop:
                break
            else:
                lock.acquire()
                self.sp.capture(self.left_border + self.board_width * (self.num * 2 + 1) / 8, self.baseline)
                lock.release()
                color = self.sp.pixel()
                if deserve_click(color):
                    pyautogui.press(FINGER_KEY[self.num])
                # if deserve_stop(color):
                #     self.hand.stop_fingers()


class Hand (object):
    def __init__(self):
        self.stop = False
        self.fingers = []

    def setup_fingers(self, left_border, board_width, baseline):
        self.fingers = []
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 0, baseline))
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 1, baseline))
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 2, baseline))
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 3, baseline))

    def stop_fingers(self):
        self.stop = True
        print 'fingers stopped'

    def start_fingers(self):
        for finger in self.fingers:
            finger.start()
        print 'fingers started'
