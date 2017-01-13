import sys
import termios
import contextlib
import pyautogui
from worker import Hand


# l is 0x6c, r is 0x72, s is 0x73, p is 0x70, y is 0x79
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
    baseline = -1
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
                    left_border = mouse_x
                    print 'left_border set to: %d' % left_border
                elif ch_str == '72':
                    mouse_x, mouse_y = pyautogui.position()
                    right_border = mouse_x
                    print 'right_border set to: %d' % right_border
                elif ch_str == '79':
                    mouse_x, mouse_y = pyautogui.position()
                    baseline = mouse_y
                    print 'baseline set to %d' % baseline
                elif ch_str == '73':
                    board_width = right_border - left_border
                    if board_width > 0:
                        if baseline > 0:
                            hand.setup_fingers(left_border, board_width, baseline)
                            hand.start_fingers()
                        else:
                            print 'wrong baseline, use \'y\' to set it'
                    else:
                        print 'wrong board width, use \'l\' and \'r\' properly again ... '
                else:
                    print 'wrong option %s' % ch_str
                    hand.stop_fingers()
                    break
        except (KeyboardInterrupt, EOFError):
            hand.stop_fingers()
        print 'bot stops'


if __name__ == '__main__':
    main()
