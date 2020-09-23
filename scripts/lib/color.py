class Color:
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    WHITE = 7

    @classmethod
    def colored(cls, string, color, bold=False):
        if type(color) == int:
            return cls.__colored(string, color, bold)
        elif type(color) == str:
            color_code = eval("Color." + color)
            return cls.__colored(string, color_code, bold)

        raise TypeError("color should be int or str.")

    @classmethod
    def __colored(cls, string, color_code, bold=False):
        return "\033[38;5;{}{}m{}\033[m".format(
            color_code, ";1" if bold else "", string
        )
