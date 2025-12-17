import random


class Goose:

    lst_id = random.sample(range(0, 50), 10)

    def __init__(self, name, balance: int = 0) -> None:
        self.name: str | None = name
        self.balance = balance

    def __repr__(self):
        return f"{type(self).__name__}(name = '{self.name}', balance = {self.balance})"

    def __add__(self, other):
        if type(self).__name__ == "Goose" and type(other).__name__ == type(self).__name__:
            flock_id = random.choice(Goose.lst_id)
            Goose.lst_id.remove(flock_id)
        else:
            raise TypeError("You can concatenate only identical gooses type")

        return GooseFlock(f"Flock{flock_id}", (self.balance + other.balance), type(self).__name__)


class WarGoose(Goose):

    def __init__(self, name, balance: int = 0) -> None:
        super().__init__(name, balance)
        self.damage = 10

    def __add__(self, other):
        if type(self).__name__ == "WarGoose" and type(other).__name__ == type(self).__name__:
            flock_id = random.choice(Goose.lst_id)
            Goose.lst_id.remove(flock_id)
        else:
            raise TypeError("You can concatenate only identical gooses type")

        return GooseFlock(f"Flock{flock_id}", (self.balance + other.balance), type(self).__name__, self.damage + other.damage)


class HonkGoose(Goose):

    def __init__(self, name, balance: int = 0) -> None:
        super().__init__(name, balance)
        self.honk_volume = 10

    def __add__(self, other):
        if type(self).__name__ == "HonkGoose" and type(other).__name__ == type(self).__name__:
            flock_id = random.choice(Goose.lst_id)
            Goose.lst_id.remove(flock_id)
        else:
            raise TypeError("You can concatenate only identical gooses type")

        return GooseFlock(f"Flock{flock_id}", (self.balance + other.balance), type(self).__name__, honk_volume=self.honk_volume + other.honk_volume)


class GooseFlock:

    def __init__(self, name, balance, goose_type, damage=0, honk_volume=0) -> None:
        self.flock = {}
        self.balance = balance
        self.name = name
        self.flock[name] = self.balance
        self.type = goose_type
        self.damage = damage
        self.honk_volume = honk_volume

    def __repr__(self) -> str:
        if self.type == "Goose":
            return f"GooseFlock(name = '{self.name}', balance = {self.balance}, type = '{self.type}')"
        elif self.type == "WarGoose":
            return f"WarGooseFlock(name = '{self.name}', balance = {self.balance}, type = '{self.type}', damage = {self.damage})"
        else:
            return f"HonkGooseFlock(name = '{self.name}', balance = {self.balance}, type = '{self.type}', honk volume = {self.honk_volume})"

    def __add__(self: "GooseFlock", other: WarGoose | HonkGoose | Goose):
        self.balance += other.balance
        self.flock[self.name] = self.balance
        return self
