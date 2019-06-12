

class Image(object):

    def __init__(self):
        self._children = None

    def _render(self, base_image):
        raise NotImplementedError()

    def _create_child(self, arg):
        raise NotImplementedError()

    def render(self, draw, args):
        for arg in args:
            if type(arg) == list:
                self._create_child(arg).render(draw, arg)
            else:
                break
        self._render(draw)


