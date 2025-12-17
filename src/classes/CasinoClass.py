from src.collections.GooseCollection import GooseCollection
from src.collections.CasinoBalanceCollection import CasinoBalance
from src.classes.PlayerClass import Player
from src.classes.GooseClasess import Goose, WarGoose, HonkGoose
from src.classes.ChipClass import Chip
from src.STATIC import ALLOWED_ACTIONS, ALLOWED_CHIPS_VALUES

import random


class Casino:

    def __init__(self, seed=None) -> None:
        if seed is not None:
            random.seed(seed)
        self.goose_collection = GooseCollection()
        self.player_collection = CasinoBalance()

    @property
    def summary_players_balance(self):
        return self.player_collection.summary_balance

    def player_registry(self, name: str, balance: int = 0):
        self.player_collection.add_player(Player(name))
        if balance != 0:
            chips = self.lay_out_for_chips(balance)
            self.player_collection[name].chips_col.add_many_chips(
                chips)
        else:
            return

    def goose_registry(self, type: str, name: str, balance: int = 0):
        if type == "Goose":
            self.goose_collection.add_goose(Goose(name, balance))
        elif type == "WarGoose":
            self.goose_collection.add_goose(WarGoose(name, balance))
        elif type == "HonkGoose":
            self.goose_collection.add_goose(HonkGoose(name, balance))
        else:
            raise TypeError("Incorrect type of goose")

    def calculate_k(self):
        rand = random.random()

        if rand < 0.01:
            return 10
        elif rand < 0.06:
            return 2
        elif rand < 0.17:
            return 1.5
        elif rand < 0.3:
            return 1
        elif rand < 0.53:
            return 0.9
        elif rand < 0.9:
            return 0.8
        else:
            return 0.7

    def lay_out_for_chips(self, value):
        """Конвертирует числовое значение в список фишек"""
        chips = []
        value = int(value)

        if value < 5:
            return chips

        for chip_value in ALLOWED_CHIPS_VALUES[::-1]:
            while value >= chip_value:
                chips.append(Chip(chip_value))
                value -= chip_value

        return chips

    def downgrade_debuffs(self):

        for player in list(self.player_collection.players.values()):
            if player.panic_ind >= 2:
                player.panic_ind -= 2
            else:
                continue

    def player_lose(self, name: str):
        self.player_collection.rm_player(name)

    def sim_step(self):

        if not self.player_collection.players or self.summary_players_balance == 0:
            return 0

        if self.player_collection.summary_balance >= 5000:
            return 1

        k = self.calculate_k()
        self.downgrade_debuffs()

        action = random.choice(ALLOWED_ACTIONS)

        print("\n" + "─" * 60)
        action_names = {
            "bet": "СТАВКИ",
            "wargoose_attack": "АТАКА БОЕВОГО ГУСЯ",
            "honkgoose_honk": "КРИК ГУСЯ",
            "goose_join": "ОБЪЕДИНЕНИЕ ГУСЕЙ"
        }
        print(f"  {action_names.get(action, action)}")
        print("─" * 60)

        if action == "bet":

            for player in list(self.player_collection.players.values()):

                if player.panic_ind >= 92:
                    player.chips_col.chips = []
                    self.player_lose(player.name)
                    print(f"  {player.name} в панике потерял все фишки и выбыл!")
                    continue

                try:
                    bet_value = player.make_bet()
                except ValueError:
                    print(f"  {player.name} не может сделать ставку и выбыл!")
                    self.player_lose(player.name)
                    continue

                bet_value *= k
                print(f"  {player.name} сделал ставку. Коэффициент: {k:.2f}x")

                # try:

                win = self.lay_out_for_chips(bet_value)
                player.chips_col.add_many_chips(win)
                if player.chips_col.summary_value >= 5:
                    if k > 1:
                        print(
                            f"  {player.name} выиграл! Новый баланс: {player.balance}")
                    else:
                        print(
                            f"  {player.name} проиграл. Новый баланс: {player.balance}")

                    lost_amount = bet_value / k
                    all_gooses = list(self.goose_collection.gooses.values(
                    )) + list(self.goose_collection.flockes.values())

                    if all_gooses:
                        share = lost_amount / len(all_gooses)
                        for goose in all_gooses:
                            goose.balance += share
                else:
                    print(f"  {player.name} проиграл и выбыл из игры!")
                    self.player_lose(player.name)

                    lost_amount = bet_value / k
                    all_gooses = list(self.goose_collection.gooses.values(
                    )) + list(self.goose_collection.flockes.values())

                    if all_gooses:
                        share = lost_amount / len(all_gooses)
                        for goose in all_gooses:
                            goose.balance += share

                    continue

        if action == "wargoose_attack":

            war_gooses = [goose for goose in (list(self.goose_collection.gooses.values(
            )) + list(self.goose_collection.flockes.values())) if (type(goose).__name__ == "WarGoose") or (type(goose).__name__ == "GooseFlock" and goose.type == "WarGoose")]

            if not war_gooses:
                print("  Нет доступных боевых гусей для атаки")
                return

            player = random.choice(
                list(self.player_collection.players.values()))

            attacker = random.choice(war_gooses)

            print(
                f"  Атакующий: {type(attacker).__name__}, имя: {attacker.name} (урон: {attacker.damage})")
            print(f"  Цель: {player.name}")

            if random.random() > player.dodge_chance:
                new_player_balance = player.balance - attacker.damage
                attacker.balance += attacker.damage

                new_chips = self.lay_out_for_chips(new_player_balance)

                player.clean_chips()

                player.chips_col.add_many_chips(new_chips)
                if player.chips_col.summary_value >= 5:
                    print(
                        f"  Удар успешен! Игрок потерял {attacker.damage}, его баланс: {player.chips_col.summary_value}")
                else:
                    print(f"  {player.name} выбыл из игры!")
                    self.player_lose(player.name)
                    return

            else:
                print(f"  {player.name} парировал атаку гуся!")

        if action == "honkgoose_honk":

            honk_gooses = [goose for goose in (list(self.goose_collection.gooses.values(
            )) + list(self.goose_collection.flockes.values())) if (type(goose).__name__ == "HonkGoose") or (type(goose).__name__ == "GooseFlock" and goose.type == "HonkGoose")]

            if not honk_gooses:
                print("  Нет доступных кричащих гусей")
                return

            player = random.choice(
                list(self.player_collection.players.values()))

            honker = random.choice(honk_gooses)

            player.panic_ind += honker.honk_volume
            print(f"  {type(honker).__name__} кричит на {player.name}!")
            print(
                f"  Паника увеличилась на {honker.honk_volume}% (всего: {player.panic_ind}%)")

        if action == "goose_join":

            if len(self.goose_collection.gooses) >= 2:
                selected_gooses = random.sample(
                    list(self.goose_collection.gooses.keys()), k=2)
                try:
                    self.goose_collection.make_flock(selected_gooses)
                    print(
                        f"  Гуси {selected_gooses[0]} и {selected_gooses[1]} объединились в стаю!")
                except TypeError:
                    print("  Невозможно создать стаю из гусей разного типа")
            else:
                print("  Недостаточно гусей для объединения (нужно минимум 2)")

    def run_simulation(self):

        print("="*20, "ЗАПУСК СИМУЛЯЦИИ", "="*20)

        while True:

            res = self.sim_step()
            if res == 1:
                break

            elif res == 0:
                break

        print("="*20, "ИТОГ", "="*20)

        if res == 1:
            print("ИГРОКИ ВЫИГРАЛИ")
        elif res == 0:
            print("ВЫИГРАЛИ ГУСИ")


# cas = Casino()

# cas.player_registry("Jhon", 250)
# print(cas.player_collection["Jhon"].chips_col.chips)
# cas.player_collection["Jhon"].chips_col.add_chip(Chip(500))
# cas.player_registry("Alice")
# cas.player_collection["Alice"].chips_col.add_chip(Chip(200))
# cas.goose_registry("WarGoose", "MJ")
# cas.goose_registry("WarGoose", "LBJ")


# print(
#     f"Игрок Jhon, баланс:{cas.player_collection["Jhon"].balance} Фишки: {cas.player_collection["Jhon"].chips_col.chips}")
# print(
#     f"Игрок Alice, баланс:{cas.player_collection["Alice"].balance} Фишки: {cas.player_collection["Alice"].chips_col.chips}")
# print(f"Стаи: {cas.goose_collection.flockes}, баланс: {cas.goose_collection.summary_goose_balance}")

# cas.sim_step()
# print(
#     f"Игрок Jhon, баланс:{cas.player_collection["Jhon"].balance}\nФишки: {cas.player_collection["Jhon"].chips_col.chips}\n")
# print(
#     f"Игрок Alice, баланс:{cas.player_collection["Alice"].balance}\nФишки: {cas.player_collection["Alice"].chips_col.chips}")

# print("Баланс казино: ", cas.summary_players_balance)
# print("Баланс гусей:", cas.goose_collection.summary_goose_balance)
