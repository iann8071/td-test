import common
from pandas import read_table
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class Character(common.Image):

    def __init__(self, char, font, font_size, x, y):
        self._char = char
        self._font = font
        self._w, self._h = font.getsize(char)
        self._x = x
        self._y = y

    def _render(self, draw):
        draw.text((self._x, self._y), self._char, font=self.font, fill='#000')


class Text(common.Image):

    def __init__(self, args):
        args_array = np.array(args)
        xs_array = args_array[:, -2]
        ys_array = args_array[:, -1]
        x_min = np.min(xs_array)
        y_min = np.min(ys_array)
        x_max = np.max(xs_array)
        y_max = np.max(ys_array)
        self._x_min = x_min
        self._y_min = y_min
        self._x_max = x_max
        self._y_max = y_max
        self._line_width = 10

    def _create_child(self, arg):
        return Character(*arg)

    def _render(self, draw):
        draw.line([self._x_min, self._y_min,self._x_max, self._y_min], fill=(255, 255, 0), width=self._line_width)
        draw.line([self._x_min, self._y_min,self._x_max, self._y_min], fill=(255, 255, 0), width=self._line_width)
        draw.line([self._x_min, self._y_min,self._x_max, self._y_min], fill=(255, 255, 0), width=self._line_width)


class Box(common.Image):
    def _render(self, base_image):
        raise NotImplementedError()

    def _create_child(self, arg):
        raise NotImplementedError()



class Document(common.Image):

    def to_image(self):
        pass


def main():
    # character = Character(1, 0, 100, 0, 0)
    # character.to_image()
    args = [
        [1, 0, 100, 0, 100],
        [1, 0, 100, 56, 100],
        [1, 0, 100, 112, 100],
        [1, 0, 100, 168, 100],
        [1, 0, 100, 220, 100]
    ]
    text = Text(args)
    image = Image.new('RGB', (1000, 1000), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    text.render(draw, args)
    image.save('test.png')


if __name__ == "__main__":
    main()