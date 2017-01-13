import threading
import pyautogui
from screenpixel import ScreenPixel


FINGER_KEY = ['d', 'f', 'j', 'k']
lock = threading.Lock()


def deserve_click(rgb):
    if rgb[0] < 10 and rgb[1] < 10 and rgb[2] < 10:
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
    def __init__(self, sp, left_border, board_width, hand, num):
        threading.Thread.__init__(self)
        self.sp = sp
        self.left_border = left_border
        self.board_width = board_width
        self.hand = hand
        self.num = num

    def run(self):
        while True:
            if self.hand.stop:
                break
            else:
                mouse_x, mouse_y = pyautogui.position()
                mouse_y -= 5
                lock.acquire()
                self.sp.capture(self.left_border + self.board_width * (self.num * 2 + 1) / 8, mouse_y)
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

    def setup_fingers(self, left_border, board_width):
        self.fingers = []
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 0))
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 1))
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 2))
        self.fingers.append(Finger(ScreenPixel(), left_border, board_width, self, 3))

    def stop_fingers(self):
        self.stop = True
        print 'fingers stopped'

    def start_fingers(self):
        for finger in self.fingers:
            finger.start()
        print 'fingers started'
