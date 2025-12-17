from src.STATIC import ALLOWED_CHIPS_VALUES


class Chip:

    def __init__(self, value) -> None:
        self.value = value

    def __add__(self, other):
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        else:
            raise TypeError(f"Can not add Chip and {type(other)}")

    def __repr__(self) -> str:
        return f"Chip({self.value})"
