import sys
import termios
import contextlib
import pyautogui
from screenpixel import ScreenPixel


def deserve_click(rgb):
    if rgb[0] == 0 and rgb[1] == 0 and rgb[2] == 0:
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
    board_width = -1
    sp = ScreenPixel()
    with raw_mode(sys.stdin):
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
                        while True:
                            mouse_x, mouse_y = pyautogui.position()
                            mouse_y -= 5

                            sp.capture(left_border+board_width/8, mouse_y)
                            color0 = sp.pixel(0, 0)
                            sp.capture(left_border+board_width*3/8, mouse_y)
                            color1 = sp.pixel(0, 0)
                            sp.capture(left_border+board_width*5/8, mouse_y)
                            color2 = sp.pixel(0, 0)
                            sp.capture(left_border+board_width*7/8, mouse_y)
                            color3 = sp.pixel(0, 0)

                            if deserve_click(color0):
                                pyautogui.press('d')
                            if deserve_click(color1):
                                pyautogui.press('f')
                            if deserve_click(color2):
                                pyautogui.press('j')
                            if deserve_click(color3):
                                pyautogui.press('k')
                    else:
                        print 'wrong board width, use \'l\' and \'r\' properly again ... '
                else:
                    print 'wrong option %s' % ch_str
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == '__main__':
    main()
