from PIL import Image, ImageDraw, ImageColor, ImageFont
import glob

def block_draw(image,column,row,height,width,fill_colour):

    #numpy array [row,column]
    #pil image [column,row]

    pixel_x = column*width
    pixel_y = row*height

    draw = ImageDraw.Draw(image)

    draw.rectangle((pixel_x,pixel_y,pixel_x+width,pixel_y+height), fill=fill_colour)

    del draw


class pretti:
    def __init__(self, initial_config, rulebook, size=None, square_size=10):

        self.num_rows = len(initial_config)
        self.num_columns = len(initial_config[0])
        self.config = initial_config

        if size == None:
            self.image = Image.new(
                mode="RGB",
                size=(self.num_columns * square_size, self.num_rows * square_size),
                color="white",
            )
            self.width_size = self.height_size = square_size

        elif (
            type(size) == list
            and len(size) == 2
            and type(size[0]) == type(size[1]) == int
        ):

            self.width_size = size[0] / self.num_columns
            self.height_size = size[1] / self.num_rows
            self.image = Image.new(
                mode="RGB",
                size=size,
                color="white",
            )

        if callable(rulebook):

            self.rulebook = rulebook
            self.__rulebook_is_function = True

        elif type(rulebook) == dict:

            self.rulebook = rulebook
            self.__rulebook_is_function = False

        else:

            raise TypeError("Rulebook must be dictionary or function.")

    def draw(self):

        for column in range(self.num_columns):
            for row in range(self.num_rows):

                if self.__rulebook_is_function:

                    fill_colour = self.rulebook(value=self.config[row][column], row=row,column=column)

                    block_draw(self.image, column, row, self.height_size, self.width_size, fill_colour)

                else:

                    fill_colour = self.rulebook[self.config[row][column]]

                    block_draw(self.image, column, row, self.height_size, self.width_size, fill_colour)

    def display(self):

        self.image.show()

if __name__ == "__main__":

    import numpy as np
    import inspect

    def color(value: float,column: int,row: int) -> str:

        rgb_string = f"hsl({360*value},100%,50%)"

        return rgb_string

    random_array = np.random.rand(5,5)
    pret = pretti(random_array,color)
    pret.draw()
    pret.display()