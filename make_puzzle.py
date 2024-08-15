import math
from PIL import Image, ImageDraw
import base64
from io import BytesIO

from algorithm import generate_from_image
import argparse


# parser
def get_args():
    parser = argparse.ArgumentParser(description='Generate puzzle from image')
    parser.add_argument('--seed', type=int, default=1, help='Seed value for random generator')
    parser.add_argument('--tabsize', type=int, default=20, help='The size of buzzle tab <40')
    parser.add_argument('--jitter', type=int, default=2, help='Jitter value for puzzle pieces')
    parser.add_argument('--xn_val', type=int, default=20, help='Number of pieces in the x direction')
    parser.add_argument('--yn_val', type=int, default=26, help='Number of pieces in the y direction')
    parser.add_argument('--image_path', type=str, default='test_img.png', help='Image file path')
    parser.add_argument('--line_color_width', type=str, default='blue', help='Customize the line color')
    parser.add_argument('--line_color_height', type=str, default='red', help='Customize the line color')
    parser.add_argument('--outline_color', type=str, default='black', help='Customize the line color')
    parser.add_argument('--line_width', type=float, default=0.7, help='Customize the line width')
    parser.add_argument('--filename', type=str, default='puzzle.svg', help='Output file name')
    parser.add_argument('--save_png', type=bool, default=True, help='Save as PNG')
    args = parser.parse_args()

    return args


if __name__ == "__main__":


    args = get_args()

    
    generate_from_image(
        args = args,
        seed_value=args.seed,
        tabsize=args.tabsize,  # The size of buzzle tab <40
        jitter=args.jitter,
        xn_val=args.xn_val,  # Number of pieces in the x direction
        yn_val=args.yn_val,  # Number of pieces in the y direction
        image_path=args.image_path,  # Replace with your image file path
        line_color_width=args.line_color_width,  # Customize the line color
        line_color_height=args.line_color_height,
        outline_color=args.outline_color,
        line_width=args.line_width,  # Customize the line width
        filename=args.filename
    )