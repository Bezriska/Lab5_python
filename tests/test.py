from src.STATIC import ALLOWED_CHIPS_VALUES
from src.classes.ChipClass import Chip


def lay_out_for_chips(value):
    chips = []

    while value > ALLOWED_CHIPS_VALUES[0]:
        for num in ALLOWED_CHIPS_VALUES[::-1]:

            if value % num < ALLOWED_CHIPS_VALUES[0]:
                chips.append(Chip(num))
                value -= num
                break
    return chips


res = lay_out_for_chips(160*0.8)
print(res)
