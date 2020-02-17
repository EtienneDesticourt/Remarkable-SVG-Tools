from collections import namedtuple
from enum import Enum


Pen = namedtuple("Pen", ["name", "brush", "opacity", "transform_width"])



class Brushes(Enum): # TODO CHANGE PLURAL
    BALLPOINT = 15
    FINELINER = 17
    MARKER = 16
    PENCIL = 14
    MECHANICAL_PENCIL = 13
    PAINTBRUSH = 12
    HIGHLIGHTER = 18


Ballpoint = Pen(name="Ballpoint", brush=Brushes.BALLPOINT, opacity=1, transform_width=lambda w: w)
Fineliner = Pen(name="Fineliner", brush=Brushes.FINELINER, opacity=1, transform_width=lambda w: w)
Marker = Pen(name="Marker", brush=Brushes.MARKER, opacity=1, transform_width=lambda w: w)
Pencil = Pen(name="Pencil", brush=Brushes.PENCIL, opacity=1, transform_width=lambda w: w)
MechanicalPencil = Pen(name="Mechanical Pencil",  brush=Brushes.MECHANICAL_PENCIL, opacity=1, transform_width=lambda w: w)
Paintbrush = Pen(name="Paintbrush", brush=Brushes.PAINTBRUSH, opacity=1., transform_width=lambda w: w)
Highlighter = Pen(name="Highlighter", brush=Brushes.HIGHLIGHTER, opacity=0.5, transform_width=lambda w: w)


PENS = {
    Brushes.BALLPOINT: Ballpoint,
    Brushes.FINELINER: Fineliner,
    Brushes.MARKER: Marker,
    Brushes.PENCIL: Pencil,
    Brushes.MECHANICAL_PENCIL: MechanicalPencil,
    Brushes.PAINTBRUSH: Paintbrush,
    Brushes.HIGHLIGHTER: Highlighter,
}


class Colour(Enum):
    BLACK = 0
    GRAY = 1
    WHITE = 2


class BrushSize(Enum):
    THIN = 1.875
    MEDIUM = 2.0
    THICK = 2.125


def get_pen(brush_type, pens, Brushes):
    pen = pens[Brushes(brush_type)]
    return pen


class Header(object):
    SIZE = 47
    STRUCT = "<43sI"

    def __init__(self, info, num_layers):
        self.info = info.decode("utf8")
        self.version = self.info.split("version=")[1] \
                                .split(" ")[0]
        self.version = int(self.version)
        self.num_layers = num_layers


class Layer(object):
    SIZE = 4
    STRUCT = "<I"

    def __init__(self, num_strokes):
        self.num_strokes = num_strokes


class Stroke(object):
    SIZE = 24
    STRUCT = "<IIIfII"

    def __init__(
        self,
        brush_type,
        colour,
        magic1,
        brush_size,
        magic2,
        num_points,
    ):
        self.brush_type = brush_type
        self.colour = colour
        self.magic1 = magic1
        self.brush_size = brush_size
        self.magic2 = magic2
        self.num_points = num_points


class Point(object):
    SIZE = 24
    STRUCT = "<ffffff"

    def __init__(
        self,
        x,
        y,
        speed,
        tilt,
        width,
        pressure
    ):
        self.x = x
        self.y = y
        self.speed = speed
        self.tilt = tilt
        self.width = width
        self.pressure = pressure

    def transform_width(self, width):
        return width
