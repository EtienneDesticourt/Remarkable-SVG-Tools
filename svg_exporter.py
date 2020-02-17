from format_structs import Header, Layer, Stroke, Colour, Point
from format_structs import PENS, Brushes, BrushSize
from format_structs import get_pen
import struct


SVG_FILE_PATTERN = """<svg xmlns="http://www.w3.org/2000/svg" height="{height}" width="{width}">
{content}
</svg>
"""


SVG_STROKE_PATTERN = '<g><path fill="{colour}" {options} d="M{points}"/></g>'
STROKE_OPTIONS_PATTERN = 'stroke="{colour}" stroke-width="{width}" stroke-linecap="{linecap}" stroke-linejoin="{linejoin}" opacity="{opacity}"'
PATH_WIDTH = {
    BrushSize.THIN: 2,
    BrushSize.MEDIUM: 4,
    BrushSize.THICK: 6,
}

STROKE_COLOURS = {
    Colour.BLACK: "#000000",
    Colour.GRAY: "#bfbfbf",
    Colour.WHITE: "#ffffff",
}

def create_svg_path(stroke, points, pen, Colour):
    brush_size = BrushSize(stroke.brush_size)

    fill_colour = Colour(stroke.colour)
    fill_colour = STROKE_COLOURS[fill_colour]
    if pen.brush != Brushes.MARKER:
        fill_colour = None

    stroke_width = PATH_WIDTH[brush_size]
    stroke_colour = Colour(stroke.colour).name
    if pen.brush == Brushes.HIGHLIGHTER:
        stroke_width = 30
        stroke_colour = "#fff3a8"
    elif pen.brush == Brushes.MARKER:
        stroke_width = 10

    options = STROKE_OPTIONS_PATTERN.format(
        colour=stroke_colour,
        width=stroke_width,
        linecap="butt",
        linejoin="round",
        opacity=pen.opacity
    )


    path = SVG_STROKE_PATTERN.format(
        colour=fill_colour,
        options=options,
        points=" ".join(["%.2f,%.2f" % (p.x, p.y) for p in points])
    )

    return path


def unpack_into(FormatStruct, f):
    struct_bytes = f.read(FormatStruct.SIZE)
    struct_info = struct.unpack(FormatStruct.STRUCT, struct_bytes)
    format_struct = FormatStruct(*struct_info)
    return format_struct


def export(input_filepath, output_filepath):
    input_file = open(input_filepath, "rb")

    header = unpack_into(Header, input_file)

    svg_contents = ""
    for layer_index in range(header.num_layers):
        layer = unpack_into(Layer, input_file)

        for stroke_index in range(layer.num_strokes):
            stroke = unpack_into(Stroke, input_file)
            pen = get_pen(stroke.brush_type, PENS, Brushes)

            points = []
            for point_index in range(stroke.num_points):
                point = unpack_into(Point, input_file)
                points.append(point)

            path = create_svg_path(stroke, points, pen, Colour)
            svg_contents += path + "\n"

    svg_contents = SVG_FILE_PATTERN.format(
        height=1872,
        width=1404,
        content=svg_contents
    )
    with open(output_filepath, "w") as f:
        f.write(svg_contents)


if __name__ == "__main__":
    export(r"data\test_page.rm", r"data\output.svg")
