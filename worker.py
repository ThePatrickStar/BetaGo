import threading
import pyautogui


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
    def __init__(self, sp, left_border, board_width, mouse_y, hand, num):
        threading.Thread.__init__(self)
        self.sp = sp
        self.left_border = left_border
        self.board_width = board_width
        self.hand = hand
        self.num = num
        self.mouse_y = mouse_y

    def run(self):
        while True:
            if self.hand.stop:
                break
            else:
                mouse_x, mouse_y = pyautogui.position()
                self.mouse_y = mouse_y - 2
                lock.acquire()
                self.sp.capture(self.left_border + self.board_width * (self.num * 2 + 1) / 8, self.mouse_y)
                lock.release()
                color = self.sp.pixel(0, 0)
                if deserve_click(color):
                    pyautogui.press(FINGER_KEY[self.num])
                # if deserve_stop(color):
                #     self.hand.stop_fingers()


class Hand (object):
    def __init__(self):
        self.stop = False

    def stop_fingers(self):
        self.stop = True
        print 'fingers stopped'
