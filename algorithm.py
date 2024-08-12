import math
from PIL import Image, ImageDraw
import base64
from io import BytesIO

def save(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

seed = 1
def random_value():
    global seed
    x = math.sin(seed) * 10000
    seed += 1
    return x - math.floor(x)

def uniform(min_val, max_val):
    return min_val + random_value() * (max_val - min_val)

def rbool():
    return random_value() > 0.5

a, b, c, d, e, t, j, flip, xi, yi, xn, yn, vertical, offset, width, height, radius = (0,)*17

def first():
    global e
    e = uniform(-j, j)
    next_piece()

def next_piece():
    global a, b, c, d, e, flip
    flipold = flip
    flip = rbool()
    a = -e if flip == flipold else e
    b = uniform(-j, j)
    c = uniform(-j, j)
    d = uniform(-j, j)
    e = uniform(-j, j)

def sl():
    return height / yn if vertical else width / xn

def sw():
    return width / xn if vertical else height / yn

def ol():
    return offset + sl() * (yi if vertical else xi)

def ow():
    return offset + sw() * (xi if vertical else yi)

def l(v):
    return round(ol() + sl() * v, 2)

def w(v):
    return round(ow() + sw() * v * (-1.0 if flip else 1.0), 2) ## add some random 

def p0l(): return l(0.0)
def p0w(): return w(0.0)
def p1l(): return l(0.2)
def p1w(): return w(a)
def p2l(): return l(0.5 + b + d)
def p2w(): return w(-t + c)
def p3l(): return l(0.5 - t + b)
def p3w(): return w(t + c)
def p4l(): return l(0.5 - 2.0 * t + b - d)
def p4w(): return w(3.0 * t + c)
def p5l(): return l(0.5 + 2.0 * t + b - d)
def p5w(): return w(3.0 * t + c)
def p6l(): return l(0.5 + t + b)
def p6w(): return w(t + c)
def p7l(): return l(0.5 + b + d)
def p7w(): return w(-t + c)
def p8l(): return l(0.8)
def p8w(): return w(e)
def p9l(): return l(1.0)
def p9w(): return w(0.0)

def gen_dh():
    global vertical, xi, yi
    vertical = 0
    path = []
    for yi in range(1, yn):
        xi = 0
        first()
        path.append(f"M {p0l()} {p0w()}")
        while xi < xn:
            path.append(f"C {p1l()} {p1w()} {p2l()} {p2w()} {p3l()} {p3w()}")
            path.append(f"C {p4l()} {p4w()} {p5l()} {p5w()} {p6l()} {p6w()}")
            path.append(f"C {p7l()} {p7w()} {p8l()} {p8w()} {p9l()} {p9w()}")
            next_piece()
            xi += 1
    return ' '.join(path)

def gen_dv():
    global vertical, xi, yi
    vertical = 1
    path = []
    for xi in range(1, xn):
        yi = 0
        first()
        path.append(f"M {p0w()} {p0l()}")
        while yi < yn:
            path.append(f"C {p1w()} {p1l()} {p2w()} {p2l()} {p3w()} {p3l()}")
            path.append(f"C {p4w()} {p4l()} {p5w()} {p5l()} {p6w()} {p6l()}")
            path.append(f"C {p7w()} {p7l()} {p8w()} {p8l()} {p9w()} {p9l()}")
            next_piece()
            yi += 1
    return ' '.join(path)

def gen_db():
    path = []
    path.append(f"M {offset + radius} {offset}")
    path.append(f"L {offset + width - radius} {offset}")
    path.append(f"A {radius} {radius} 0 0 1 {offset + width} {offset + radius}")
    path.append(f"L {offset + width} {offset + height - radius}")
    path.append(f"A {radius} {radius} 0 0 1 {offset + width - radius} {offset + height}")
    path.append(f"L {offset + radius} {offset + height}")
    path.append(f"A {radius} {radius} 0 0 1 {offset} {offset + height - radius}")
    path.append(f"L {offset} {offset + radius}")
    path.append(f"A {radius} {radius} 0 0 1 {offset + radius} {offset}")
    return ' '.join(path)

def embed_image_in_svg(image_path):
    """Embed the image as a base64 string in the SVG."""
    image = Image.open(image_path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f'<image href="data:image/png;base64,{img_str}" width="{width}" height="{height}" />'

def generate_from_image(seed_value, tabsize, jitter, xn_val, yn_val, image_path, line_color_width = "black" , line_color_height="black" , outline_color = "black", line_width=0.1, filename="jigsaw.svg"):
    global seed, t, j, xn, yn, width, height, radius, offset
    seed = seed_value
    t = tabsize / 200.0
    j = jitter / 100.0
    xn = xn_val
    yn = yn_val
    radius = 0  # Adjust radius for puzzle pieces if necessary
    offset = 0.0

    # Load the image and get its dimensions
    image = Image.open(image_path)
    width, height = image.size  # Use the image dimensions for the puzzle size

    print(f"Image width and height = {width} mm × {height}mm\n")

    # Embed the image in the SVG
    embedded_image = embed_image_in_svg(image_path)

    svg_content = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.0\" "
    svg_content += f"width=\"{width}mm\" height=\"{height}mm\" viewBox=\"0 0 {width} {height}\">"
    svg_content += embedded_image  # Add the embedded image as the bottom layer
    svg_content += f"<path fill=\"none\" stroke=\"{line_color_width}\" stroke-width=\"{line_width}\" d=\"{gen_dh()}\"></path>"
    svg_content += f"<path fill=\"none\" stroke=\"{line_color_height}\" stroke-width=\"{line_width}\" d=\"{gen_dv()}\"></path>"
    svg_content += f"<path fill=\"none\" stroke=\"{outline_color}\" stroke-width=\"{line_width}\" d=\"{gen_db()}\"></path>"
    svg_content += "</svg>"

    save(filename, svg_content)






