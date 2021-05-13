from PIL import Image, ImageDraw, ImageColor, ImageFont
import glob


def block_draw(image, column, row, height, width, fill_colour):

    # numpy array [row,column]
    # pil image [column,row]

    pixel_x = column * width
    pixel_y = row * height

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (pixel_x, pixel_y, pixel_x + width, pixel_y + height), fill=fill_colour
    )

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

                    fill_colour = self.rulebook(
                        value=self.config[row][column],
                        row=row,
                        column=column,
                        max_column=self.num_columns,
                        max_row=self.num_rows,
                    )

                    block_draw(
                        self.image,
                        column,
                        row,
                        self.height_size,
                        self.width_size,
                        fill_colour,
                    )

                else:

                    fill_colour = self.rulebook[self.config[row][column]]

                    block_draw(
                        self.image,
                        column,
                        row,
                        self.height_size,
                        self.width_size,
                        fill_colour,
                    )

    def display(self):

        self.image.show()

    def save(self):

        self.image.save("{}".format(path))


def rule_num_to_dictionary(number):

    return_dict = {}

    keys = ["111", "110", "101", "100", "011", "010", "001", "000"]

    raw_bin = bin(number)[2:].zfill(8)

    for i in range(8):

        return_dict[keys[i]] = raw_bin[i]

    print(return_dict)

    return return_dict


def next_row(row, rule_dict):

    return_row = row

    for i in range(0, len(row)):

        if i == 0:

            key = f"0{int(row[i])!r}{int(row[i+1])!r}"

        elif i == (len(row) - 1):

            key = f"{int(row[-2])!r}{int(row[-1])!r}0"

        else:

            key = f"{int(row[i-1])!r}{int(row[i])!r}{int(row[i+1])!r}"

        return_row[i] = int(rule_dict[key])

    return return_row


def wolfram_rule_array(rule_num: int, rows: int, start_row: list):

    return_array = np.zeros((rows, len(start_row)))

    rule_dict = rule_num_to_dictionary(rule_num)

    return_array[0] = start_row

    for i in range(1, rows):

        return_array[i] = next_row(return_array[i - 1], rule_dict)

    return return_array


if __name__ == "__main__":

    import numpy as np
    import inspect

    # def color(**kwargs) -> str:

    #     row_ratio = kwargs['row']/kwargs['max_row']

    #     column_ratio = kwargs['column']/kwargs['max_column']

    #     rgb_string = f"hsl({360*kwargs['value']},100%,{50*column_ratio*row_ratio}%)"

    #     return rgb_string

    # random_array = np.random.rand(100, 100)
    # pret = pretti(random_array, color)
    # pret.draw()
    # pret.display()

    start_row = np.random.choice(2, 200)

    #start_row = np.zeros((100))

    start_row[49] = 1

    tmp_array = wolfram_rule_array(137, 200, start_row)

    pret = pretti(tmp_array, {0: "white", 1: "pink"})
    pret.site_size = 5
    pret.draw()
    pret.display()