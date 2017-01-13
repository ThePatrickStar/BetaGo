import sys
import termios
import contextlib
import pyautogui
from screenpixel import ScreenPixel
from worker import Finger, Hand


def deserve_click(rgb):
    if rgb[0] < 10 and rgb[1] < 10 and rgb[2] < 10:
        return True
    else:
        return False


# l is 0x6c, r is 0x72, s is 0x73, p is 0x70
@contextlib.contextmanager
def raw_mode(fd):
    old_attrs = termios.tcgetattr(fd.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(fd.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(fd.fileno(), termios.TCSADRAIN, old_attrs)


def main():
    print 'exit with ^C or ^D'
    left_border = -1
    right_border = -1
    with raw_mode(sys.stdin):
        hand = Hand()
        try:
            while True:
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break
                ch_str = '%02x' % ord(ch)
                if ch_str == '6c':
                    mouse_x, mouse_y = pyautogui.position()
                    print 'mouse x %d' % mouse_x
                    print 'mouse y %d' % mouse_y
                    left_border = mouse_x
                    print 'left_border set to: %d' % left_border
                elif ch_str == '72':
                    mouse_x, mouse_y = pyautogui.position()
                    print 'mouse x %d' % mouse_x
                    print 'mouse y %d' % mouse_y
                    right_border = mouse_x
                    print 'right_border set to: %d' % right_border

                elif ch_str == '73':
                    print 'starting bot ...'
                    board_width = right_border - left_border
                    if board_width > 0:
                        mouse_x, mouse_y = pyautogui.position()
                        mouse_y -= 2

                        sp0 = ScreenPixel()
                        sp1 = ScreenPixel()
                        sp2 = ScreenPixel()
                        sp3 = ScreenPixel()
                        finger0 = Finger(sp0, left_border, board_width, mouse_y, hand, 0)
                        finger1 = Finger(sp1, left_border, board_width, mouse_y, hand, 1)
                        finger2 = Finger(sp2, left_border, board_width, mouse_y, hand, 2)
                        finger3 = Finger(sp3, left_border, board_width, mouse_y, hand, 3)
                        finger0.start()
                        finger1.start()
                        finger2.start()
                        finger3.start()
                    else:
                        print 'wrong board width, use \'l\' and \'r\' properly again ... '
                else:
                    print 'wrong option %s' % ch_str
                    hand.stop_fingers()
        except (KeyboardInterrupt, EOFError):
            hand.stop_fingers()


if __name__ == '__main__':
    main()
