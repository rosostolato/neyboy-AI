from math import sqrt
from PIL.Image import Image
import math


class Point2d:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def distanceto(self, b, axis=None):
        if (axis == 'x'):
            return b.x - self.x
        if (axis == 'y'):
            return b.y - self.y
        if (axis == 'all'):
            return b.x - self.x, b.y - self.y

        return sqrt((b.x-self.x)**2+(b.y-self.y)**2)

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def getbox(self):
        return (self.left, self.top, self.left +
                self.width, self.top + self.height)

    def __repr__(self):
        return 'Rect(left:{}, top:{}, width:{}, height:{})'\
            .format(self.left, self.top, self.width, self.height)


class Pixel:
    def __init__(self, image: Image, coord=(0, 0)):
        self.x, self.y = coord
        self._image = image

    def isvalid(self):
        overflow = (self.x >= self._image.width or
                    self.y >= self._image.height)
        underflow = (self.x < 0 or self.y < 0)
        return not (overflow or underflow)

    def getcolor(self):
        if (not self.isvalid()):
            return (0, 0, 0)
        return self._image.getpixel((self.x, self.y))

    def getneighbors(self):
        pixels = []

        for k in range(8):
            xy = (self.x + int(round(math.sin(k * math.pi/4))),
                  self.y - int(round(math.cos(k * math.pi/4))))

            pix = Pixel(self._image, xy)
            pixels.append(pix)

        return pixels

    def findpixel(self, color: tuple, direction: float, distmax=50):
        x, y = self.x, self.y

        while(distmax > 0):
            xy = (x + int(round(math.cos(direction * math.pi/4))),
                  y - int(round(math.sin(direction * math.pi/4))))

            nextpix = Pixel(self._image, xy)

            if (not nextpix.isvalid()):
                return None

            if (nextpix.getcolor() == color):
                return nextpix

            distmax -= 1
            x, y = xy

        return None

        # if (distmax == 0):
        #     return None

        # xy = (self.x + int(round(math.cos(direction * math.pi/4))),
        #       self.y - int(round(math.sin(direction * math.pi/4))))

        # nextpix = Pixel(self._image, xy)

        # if (not nextpix.isvalid()):
        #     return None

        # if (nextpix.getcolor() == color):
        #     return nextpix
        # else:
        #     distmax -= 1
        #     return nextpix.findpixel(color, direction, distmax)

    def __repr__(self):
        return 'Pixel({}, {}) | Color{}'\
            .format(self.x, self.y, self.getcolor())
