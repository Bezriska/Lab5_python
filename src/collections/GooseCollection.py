from src.logger import logger
from src.classes.GooseClasess import Goose, WarGoose, HonkGoose


class GooseCollection:

    def __init__(self) -> None:
        self.gooses = {}
        self.flockes = {}

    @property
    def summary_goose_balance(self):
        goose_balance = sum(goose.balance for goose in self.gooses.values())
        flock_balance = sum(flock.balance for flock in self.flockes.values())
        return goose_balance + flock_balance

    def __iter__(self):
        return iter(self.gooses)

    def __len__(self) -> int:
        return len(self.gooses)

    def __getitem__(self, name):
        if name in self.gooses:
            return self.gooses[name]
        else:
            logger.error(f"Goose with name {name} does not found")
            raise KeyError(f"Goose with name {name} does not found")

    def __setitem__(self, name, balance):
        bal = self.gooses[name].balance
        self.gooses[name].balance = balance
        logger.info(
            f"{name}'s balance has been changed from {bal} to {balance}")

    def add_goose(self, goose: Goose | WarGoose | HonkGoose):
        self.gooses[goose.name] = goose

    def rm_goose(self, name):
        if name in self.gooses:
            del self.gooses[name]
        else:
            logger.error("Incorrect name")
            raise KeyError("Incorrect name")

    def make_flock(self, gooses_names: list[str]):
        if len(gooses_names) < 2:
            raise ValueError("Flock include min 2 gooses")

        flock = self.gooses[gooses_names[0]] + self.gooses[gooses_names[1]]

        self.rm_goose(gooses_names[0])
        self.rm_goose(gooses_names[1])

        for name in gooses_names[2:]:
            flock += self.gooses[name]
            self.rm_goose(name)

        self.flockes[flock.name] = flock

        return flock


# GooseCol = GooseCollection()

# GooseCol.add_goose(Goose("Jhon", 50))
# GooseCol.add_goose(Goose("Yarik", 250))
# GooseCol.add_goose(Goose("Yar", 300))

# flock = GooseCol.make_flock(["Jhon", "Yarik"])
# print(GooseCol.gooses)
# print(flock, GooseCol.summary_goose_balance)
