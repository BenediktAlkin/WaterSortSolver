class _Color:
    EMPTY = 0
    RED = 1
    GREEN = 2
    BLUE = 3

    def __init__(self):
        super().__init__()
        self.str_to_int = {key: getattr(self, key) for key in vars(_Color) if not key.startswith("__")}
        self.char_to_int = {key[0]: value for key, value in self.str_to_int.items()}
        self.int_to_str = {value: key for value, key in self.str_to_int.items()}
        self.int_to_char = {value: key[0] for key, value in self.str_to_int.items()}


Color = _Color()
