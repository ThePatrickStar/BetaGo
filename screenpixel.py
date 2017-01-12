import Quartz.CoreGraphics as CG
import struct


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