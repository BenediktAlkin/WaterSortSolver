class _Color:
    COLORS = [
        "EMPTY",
        "RED",
        "GREEN",
        "BLUE",
        "PINK",
        "GRAY",
        "PURPLE",
        "DARK_PURPLE",
        "DARK_BLUE",
        "TURQUOISE",
        "ORANGE",
        "DARK_RED",
        "DARK_GREEN",
        "YELLOW",
    ]

    def __init__(self):
        super().__init__()
        assert len(set(self.COLORS)) == len(self.COLORS), "colors need to be unique"
        for i, color in enumerate(self.COLORS):
            setattr(_Color, color, i)
        assert self.EMPTY == 0
        self.str_to_int = {value: key for key, value in enumerate(self.COLORS)}
        self.char_to_int = {key[0]: value for key, value in self.str_to_int.items()}
        self.int_to_str = {value: key for value, key in self.str_to_int.items()}
        self.int_to_char = {value: key[0] for key, value in self.str_to_int.items()}


Color = _Color()
