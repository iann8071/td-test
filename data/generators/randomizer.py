import numpy as np
from pandas import read_csv
from numpy.random import rand, randint, normal
from emcee import EnsembleSampler
from PIL import Image, ImageDraw, ImageFont


class BoxRandomizer(object):

    """
    params:
        length
        font
        color
        size
    """

    charset = read_csv('charset.tsv', sep='\t')
    fontset = read_csv('fontset.tsv', sep='\t')

    def run(self, x, y, draw):
        font_idx = 2
        font_color = "#000"
        font_size = int(normal(10, 2))
        length = 10
        font_name = self.fontset.loc[self.fontset['index'] == font_idx]['font1'].values[0]
        font = ImageFont.truetype('/Library/Fonts/' + font_name, font_size)
        w, h = font.getsize('a')

        max_x = x + length * w
        max_y = y + 1 * h

        box_x = x - randint(0, 10)
        box_y = y - randint(0, 10)
        box_w = (max_x - x) * (1 + rand())
        box_h = (max_y - y) * (1 + rand())
        box_color = (200, 200, 200)
        draw.rectangle((box_x, box_y, box_x + box_w, box_y + box_h), fill=box_color)

        _x = x
        _y = y
        for i in range(length):
            char_idx = randint(0, 4)
            char = self.charset.loc[self.charset['index'] == char_idx]['char1'].values[0]
            draw.text([_x, _y], char, font=font, fill=font_color)
            _x += w
            _y += 0
        _y += h

        # get convex full
        line_color = (255, 255, 0)
        line_width = 1
        draw.line((x, y, _x, y), fill=line_color, width=line_width)
        draw.line((_x, y, _x, _y), fill=line_color, width=line_width)
        draw.line((_x, _y, x, _y), fill=line_color, width=line_width)
        draw.line((x, _y, x, y), fill=line_color, width=line_width)


def main():
    max_x = 1000
    max_y = 1000
    image = Image.new('RGB', (max_x, max_y), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    randomizer = BoxRandomizer()
    n_iteration = 100

    for i in range(n_iteration):
        x = max_x * rand()
        y = max_y * rand()
        randomizer.run(x, y, draw)
    image.save('test.png')


if __name__ == "__main__":
    main()






