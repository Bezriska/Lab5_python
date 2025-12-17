from src.collections.ChipCollection import ChipCollection, Chip
import random


class Player:

    def __init__(self, name: str) -> None:
        self.name = name
        self.dodge_chance = 0.1
        self.panic_ind = 0
        self.chips_col = ChipCollection()

    @property
    def balance(self):
        return self.chips_col.summary_val

    def __repr__(self):
        return f"Player(name = {self.name}, balance = {self.balance})"

    def make_bet(self):
        if not self.chips_col.chips:
            raise ValueError("No chips available for betting")
        chip = random.choice(self.chips_col.chips)
        bet_value = chip.value
        self.chips_col.remove_chip(bet_value)
        return bet_value

    def clean_chips(self):
        self.chips_col.chips = []

