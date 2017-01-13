import Quartz.CoreGraphics as CG
import struct


class ScreenPixel(object):

    def __init__(self):
        self._data = None

    def capture(self, x, y):

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

    def pixel(self):

        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are four (blue,green,red,alpha)
        data_format = "BBBB"

        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=0)

        # Return BGRA as RGBA
        return (r, g, b)
