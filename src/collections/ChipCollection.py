from src.classes.ChipClass import Chip


class ChipCollection:

    def __init__(self) -> None:
        self.chips = []

    @property
    def summary_value(self):
        """Вычисляет общую стоимость всех фишек"""
        return sum(chip.value for chip in self.chips)

    def __iter__(self):
        return iter(self.chips)

    def __len__(self):
        return len(self.chips)

    def __getitem__(self, start=None, end=None, step=None):
        return self.chips[start:end:step]

    def __repr__(self):
        return f"ChipCollection(chips={self.chips}, total={self.summary_value})"

    def add_chip(self, chip: Chip):
        self.chips.append(chip)

    def add_many_chips(self, chips: list[Chip]):
        for chip in chips:
            self.chips.append(chip)

    def remove_chip(self, value):
        for i, chip in enumerate(self.chips):
            if chip.value == value:
                self.chips.pop(i)
                return
        raise ValueError(f"Chip with value {value} not found")
