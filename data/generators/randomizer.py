import numpy as np
from pandas import read_csv
from numpy.random import rand, randint, normal, exponential
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

    def run(self, x, y, bg_color, draw):
        font_idx = 2
        font_color = "#000"
        font_size = int(normal(10, 5))
        length = int(normal(10, 2))
        font_name = self.fontset.loc[self.fontset['index'] == font_idx]['font1'].values[0]
        font = ImageFont.truetype('/Library/Fonts/' + font_name, font_size)
        w, h = font.getsize('a')

        max_x = x + length * w
        max_y = y + 1 * h

        box_x = x - randint(0, 10)
        box_y = y - randint(0, 10)
        box_w = (max_x - box_x) * (1 + rand())
        box_h = (max_y - box_y) * (1 + rand())

        box_color = (bg_color[0] + normal(0, 2), bg_color[1] + normal(0, 2), bg_color[2] + normal(0, 2))
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
        line_color = (255, 0, 0)
        line_width = 1
        draw.line((x, y, _x, y), fill=line_color, width=line_width)
        draw.line((_x, y, _x, _y), fill=line_color, width=line_width)
        draw.line((_x, _y, x, _y), fill=line_color, width=line_width)
        draw.line((x, _y, x, y), fill=line_color, width=line_width)

        return box_x, box_y, box_x + box_w, box_y + box_h


def main():
    max_x = 1000
    max_y = 1000
    bg_color = (255 - exponential(10, 1), 255 - exponential(10, 1), 255 - exponential(10, 1))
    image = Image.new('RGB', (max_x, max_y), bg_color)
    draw = ImageDraw.Draw(image)
    randomizer = BoxRandomizer()
    n_iteration = 100

    boxes = []
    for i in range(n_iteration):
        x = max_x * rand()
        y = max_y * rand()
        box_x1, box_y1, box_x2, box_y2 = randomizer.run(x, y, bg_color, draw)
        new_box = [box_x1, box_y1, box_x2, box_y2]
        is_intersect = False
        for box in boxes:
            if intersect(box, new_box):
                is_intersect = True
                break

        if not is_intersect:
            boxes.append(new_box)
            print(boxes)
    image.save('test.png')


def intersect(box1, box2):
    is_intersect = True

    if (box1[0] > box2[0] or box1[2] < box2[0]) and \
        (box1[0] > box2[2] or box1[2] < box2[2]) and \
        (box1[1] > box2[1] or box1[3] < box2[1]) and \
        (box1[1] > box2[3] or box1[3] < box2[3]):
        is_intersect = False

    return is_intersect


if __name__ == "__main__":
    main()






