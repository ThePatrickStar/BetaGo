import sys
import termios
import contextlib
import autopy
import time
import pyscreeze
import pyautogui
import Quartz.CoreGraphics as CG
import struct


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
    mouse_y = -1
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
                    print 'mouse x %d' % autopy.mouse.get_pos()[0]
                    print 'mouse y %d' % autopy.mouse.get_pos()[1]
                    left_border = autopy.mouse.get_pos()[0]
                    print 'left_border set to: %d' % left_border
                elif ch_str == '72':
                    print 'mouse x %d' % autopy.mouse.get_pos()[0]
                    print 'mouse y %d' % autopy.mouse.get_pos()[1]
                    right_border = autopy.mouse.get_pos()[0]
                    print 'right_border set to: %d' % right_border

                elif ch_str == '73':
                    print 'starting bot ...'
                    board_width = right_border - left_border
                    if board_width > 0:
                        mid_points = [left_border+board_width/8, left_border+board_width*3/8, left_border+board_width*5/8, left_border+board_width*7/8]

                        while True:
                            mouse_y = autopy.mouse.get_pos()[1]
                            mouse_y -= 5

                            # im = pyscreeze.screenshot(region=(left_border*2, mouse_y*2, board_width*2, 1))
                            # color0 = im.getpixel((board_width / 4, 0))
                            # color1 = im.getpixel((board_width * 3 / 4, 0))
                            # color2 = im.getpixel((board_width * 5 / 4, 0))
                            # color3 = im.getpixel((board_width * 7 / 4, 0))

                            # sp.capture(left_border*2, mouse_y*2, board_width*2)
                            # color0 = sp.pixel(board_width / 4, 0)
                            # color1 = sp.pixel(board_width * 3 / 4, 0)
                            # color2 = sp.pixel(board_width * 5 / 4, 0)
                            # color3 = sp.pixel(board_width * 7 / 4, 0)

                            # sp.capture(left_border, mouse_y, board_width)
                            sp.capture(left_border+board_width/8, mouse_y)
                            color0 = sp.pixel(0, 0)
                            sp.capture(left_border+board_width*3/8, mouse_y)
                            color1 = sp.pixel(0, 0)
                            sp.capture(left_border+board_width*5/8, mouse_y)
                            color2 = sp.pixel(0, 0)
                            sp.capture(left_border+board_width*7/8, mouse_y)
                            color3 = sp.pixel(0, 0)


                            # im0 = pyscreeze.screenshot(region=(mid_points[0] * 2, mouse_y * 2, 1, 1))
                            # im1 = pyscreeze.screenshot(region=(mid_points[1] * 2, mouse_y * 2, 1, 1))
                            # im2 = pyscreeze.screenshot(region=(mid_points[2] * 2, mouse_y * 2, 1, 1))
                            # im3 = pyscreeze.screenshot(region=(mid_points[3] * 2, mouse_y * 2, 1, 1))
                            #
                            # color0 = im0.getpixel((0, 0))
                            # color1 = im1.getpixel((0, 0))
                            # color2 = im2.getpixel((0, 0))
                            # color3 = im3.getpixel((0, 0))
                            # color0 = autopy.bitmap.capture_screen().get_color(mid_points[0], mouse_y)
                            # color1 = autopy.bitmap.capture_screen().get_color(mid_points[1], mouse_y)
                            # color2 = autopy.bitmap.capture_screen().get_color(mid_points[2], mouse_y)
                            # color3 = autopy.bitmap.capture_screen().get_color(mid_points[3], mouse_y)

                            # print '====='
                            # print color0, (mid_points[0], mouse_y)
                            # print color1, (mid_points[1], mouse_y)
                            # print color2, (mid_points[2], mouse_y)
                            # print color3, (mid_points[3], mouse_y)
                            # print color0, (mid_points[0]*2, mouse_y*2)
                            # print color1, (mid_points[1]*2, mouse_y*2)
                            # print color2, (mid_points[2]*2, mouse_y*2)
                            # print color3, (mid_points[3]*2, mouse_y*2)

                            # color0 = autopy.color.hex_to_rgb(color0)
                            # color1 = autopy.color.hex_to_rgb(color1)
                            # color2 = autopy.color.hex_to_rgb(color2)
                            # color3 = autopy.color.hex_to_rgb(color3)

                            if color0[0] < 10 and color0[1] < 10 and color0[2] < 10:
                                pyautogui.press('d')
                                # autopy.mouse.move(mid_points[0], mouse_y)
                                # autopy.mouse.click()
                                # print 'click 0'
                            if color1[0] < 10 and color1[1] < 10 and color1[2] < 10:
                                pyautogui.press('f')
                                # autopy.mouse.move(mid_points[1], mouse_y)
                                # autopy.mouse.click()
                                # print 'click 1'
                            if color2[0] < 10 and color2[1] < 10 and color2[2] < 10:
                                pyautogui.press('j')
                                # autopy.mouse.move(mid_points[2], mouse_y)
                                # autopy.mouse.click()
                                # print 'click 2'
                            if color3[0] < 10 and color3[1] < 10 and color3[2] < 10:
                                pyautogui.press('k')
                                # autopy.mouse.move(mid_points[3], mouse_y)
                                # autopy.mouse.click()
                                # print 'click 3'

                            # time.sleep(0.01)
                    else:
                        print 'wrong board width, use \'l\' and \'r\' properly again ... '
                else:
                    print 'wrong option %s' % ch_str
        except (KeyboardInterrupt, EOFError):
            pass


class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    [crg:]
    ... pass two arguments to script (no comma, no nuthin', a la:
    ./thisScript.py 112 767
    """

    def capture(self, x, y):
        """see original version for capturing full screen
        (and lots of other stuff)
        """

        # if w % 2 == 1:
        #     w += 1

        region = CG.CGRectMake(x, y, 1, 1)

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)

        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

    def pixel(self, x, y):
        """Get pixel value at given (x,y) screen coordinates

        Must call capture first.
        """

        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are four (blue,green,red,alpha)
        data_format = "BBBB"

        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/

        # [crg]: removed this -- unnecessary step, just using zero
        # offset = 4 * ((self.width*int(round(y))) + int(round(x)))

        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=0)

        # Return BGRA as RGBA
        return (r, g, b)
        # can (used to) return alpha, too, but in this context, unnecessary


if __name__ == '__main__':
    main()
