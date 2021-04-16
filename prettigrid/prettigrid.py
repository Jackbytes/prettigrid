from PIL import Image, ImageDraw, ImageColor, ImageFont
import glob


class pretti(self):
    def __init__(self):

        pass

    def update(self, config):

        pass

    def new_rulebook(self, rulebook):

        if callable(rulebook):

            pass

        elif type(rulebook) == dict:

            pass

        else:

            raise TypeError("Rulebook must be dictionary or function.")