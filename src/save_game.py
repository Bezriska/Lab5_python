from src.classes.PlayerClass import Player
from src.classes.GooseClasess import Goose, WarGoose, HonkGoose, GooseFlock
from src.classes.CasinoClass import Casino

import json


def save_game(seed_name: str, players: list[Player], gooses: list[Goose | WarGoose | HonkGoose], seed: int):
    try:
        with open("src/saved_seeds.json", "r") as data:
            saves = json.load(data)
    except (FileNotFoundError, json.JSONDecodeError):
        saves = {"seeds": {}}

    if not (players and gooses and seed_name):
        return

    new_save = {
        "players": {},
        "gooses": {},
        "seed": str(seed)
    }

    for i, player in enumerate(players, 1):

        new_save["players"][f"player{i}"] = {
            "balance": player.balance,
            "name": player.name
        }

    for i, goose in enumerate(gooses, 1):

        new_save["gooses"][f"goose{i}"] = {
            "name": goose.name,
            "type": type(goose).__name__
        }

    saves["seeds"][seed_name] = new_save

    with open("src/saved_seeds.json", "w") as file:
        json.dump(saves, file, indent=4, ensure_ascii=False)


def register_players_from_save(filepath: str, save_name: str, casic: Casino):

    with open(filepath, "r") as data:
        save = json.load(data)

    for player_data in save["seeds"][save_name]["players"].values():

        name = player_data["name"]
        balance = int(player_data["balance"])  # Преобразуем в число

        casic.player_registry(name, balance)
    return


def register_gooses_from_save(filepath: str, save_name: str, casic: Casino):

    with open(filepath, "r") as data:
        save = json.load(data)

    for goose_data in save["seeds"][save_name]["gooses"].values():

        name = goose_data["name"]
        goose_type = goose_data["type"]

        casic.goose_registry(goose_type, name)
    return


with open("src/saved_seeds.json", "r") as data:
    saves = json.load(data)

print(saves["seeds"]["save1"]["players"])

for player_data in saves["seeds"]["save1"]["players"].values():
    balance = player_data["balance"]
    print(balance)

# casic = Casino()

# casic.player_registry("Alice", 100)
# casic.player_registry("Jhon", 200)

# casic.goose_registry("WarGoose", "MJ")

# save_game("lol", list(casic.player_collection.players.values()), list(
#     casic.goose_collection.gooses.values()), list(casic.goose_collection.flockes.values()), 2341)


# with open("saved_seeds.json", "r") as data:
#     saves = json.load(data)
# for i, save in enumerate(saves["seeds"]):
#     print(f"{i}) {save}")
