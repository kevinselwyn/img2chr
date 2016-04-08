#!/usr/bin/python

import math
import os
import sys
from PIL import Image

colors = [0, 0x55, 0xAA, 0xFF]
extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


def load_img(filename):
    img = Image.open(filename)

    return img


def save_chr(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)


def get_color(pixel):
    rgb = math.floor((pixel[0] + pixel[1] + pixel[2]) / 3)
    color = colors.index(min(colors, key=lambda x: abs(x - rgb)))

    return color


def str2bin(string):
    output = bytearray()

    for x in range(0, len(string), 8):
        output.append(int(string[x:x+8], 2))

    return output


def img2bin(img):
    width, height = img.size
    pixel = img.load()
    color = 0
    binary = ''

    for h in range(0, height, 8):
        for w in range(0, width, 8):
            lo = ''
            hi = ''

            for y in range(h, h + 8):
                for x in range(w, w + 8):
                    color = get_color(pixel[x, y])
                    lo += str(color & 0x01)
                    hi += str((color >> 1) & 0x01)

            binary += lo + hi

    return binary


def usage(program=os.path.basename(__file__)):
    print 'python %s <img>' % program


def main(argc, argv):
    if argc < 2 or argv[1] in ('-h', '--help'):
        usage(argv[0])
        sys.exit(1)

    input_filename = argv[1]
    output_filename = input_filename.rsplit('.', 1)[0] + '.chr'

    if input_filename.endswith(extensions) != True:
        raise Exception('Invalid image extension')
        sys.exit(1)

    img = load_img(input_filename)
    binary = img2bin(img)
    output = str2bin(binary)
    save_chr(output_filename, output)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)