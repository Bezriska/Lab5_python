from src.classes.PlayerClass import Player
from src.logger import logger
from src.collections.ChipCollection import ChipCollection


class CasinoBalance:

    def __init__(self) -> None:
        self.players = {}

    @property
    def summary_balance(self):
        return sum(player.balance for player in self.players.values())

    def __iter__(self):
        return iter(self.players)

    def __len__(self) -> int:
        return len(self.players)

    def __getitem__(self, name) -> Player:
        if name in self.players:
            return self.players[name]
        else:
            raise KeyError(f"Player with name {name} does not found")

    def __setitem__(self, name, balance):
        bal = self.players[name].balance
        self.players[name].balance = balance
        logger.info(
            f"{name}'s balance has been changed from {bal} to {balance}")

    def add_player(self, player: Player):
        self.players[player.name] = player

    def rm_player(self, name):
        if name in self.players:
            del self.players[name]
        else:
            raise KeyError("Incorrect name")


# sum_balance = CasinoBalance()
# sum_balance.add_player(Player("Alice"))
# sum_balance.add_player(Player("Petr"))
# sum_balance.rm_player("Alice")

# print(sum_balance["Petr"])
# print(sum_balance.summary_balance)
