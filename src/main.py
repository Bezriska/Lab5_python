from src.classes.CasinoClass import Casino
from src.STATIC import ALLOWED_CHIPS_VALUES
from src.save_game import save_game, register_gooses_from_save, register_players_from_save
import json
import time
from copy import deepcopy


def print_header():
    """Выводит красивый заголовок программы"""
    print("\n" + "="*60)
    print(" " * 17 + "СИМУЛЯТОР КАЗИНО")
    print("="*60 + "\n")


def print_statistics(casic):
    """Выводит красивую статистику игры"""
    print("\n" + "="*60)
    print(" " * 22 + "СТАТИСТИКА")
    print("="*60)

    print("\nИГРОКИ:")
    print("-" * 60)
    if casic.player_collection.players:
        for player_name, player in casic.player_collection.players.items():
            print(f"  {player_name}")
            print(f"     Баланс: {player.balance}")
            print(f"     Фишки: {player.chips_col.chips}")
            print(f"     Паника: {player.panic_ind}%")
            print("-" * 60)
    else:
        print("  Все игроки выбыли из игры")
        print("-" * 60)

    print(f"\nОбщий баланс игроков: {casic.summary_players_balance}")

    print("\nГУСИ:")
    print("-" * 60)
    if casic.goose_collection.gooses:
        for goose_name, goose in casic.goose_collection.gooses.items():
            goose_type = type(goose).__name__
            print(f"  {goose_name} ({goose_type})")
            print(f"     Баланс: {goose.balance}")
            if goose_type == "WarGoose":
                print(f"     Урон: {goose.damage}")
            elif goose_type == "HonkGoose":
                print(f"     Громкость: {goose.honk_volume}")
            print("-" * 60)

    if casic.goose_collection.flockes:
        print("\nСТАИ ГУСЕЙ:")
        print("-" * 60)
        for flock_name, flock in casic.goose_collection.flockes.items():
            print(f"  {flock_name} (Стая {flock.type})")
            print(f"     Баланс: {flock.balance}")
            print("-" * 60)

    print(
        f"\nОбщий баланс гусей: {casic.goose_collection.summary_goose_balance}")
    print("\n" + "="*60 + "\n")


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    print_header()
    print("ХОТИТЕ ВЫБРАТЬ ОДНУ ИЗ СОХРАНЕННЫХ СИМУЛЯЦИЙ?")

    ans = input("y/n: ")
    if ans == "y":
        with open("src/saved_seeds.json", "r") as data:
            saves = json.load(data)

        for i, save in enumerate(saves["seeds"]):
            print(f"{i}) {save}")

        num = input("\n    ВЫБЕРИТЕ НОМЕР СОХРАНЕНИЯ: ")

        for i, save in enumerate(saves["seeds"]):
            if i == int(num):
                save_name = save
                seed = saves["seeds"][save_name]["seed"]
                break
            else:
                continue

        casic = Casino(int(seed))

        register_players_from_save("src/saved_seeds.json", save_name, casic)
        register_gooses_from_save("src/saved_seeds.json", save_name, casic)

        print("\n" + "="*60)
        print("РЕЖИМ СИМУЛЯЦИИ")
        print("-" * 60)

        while True:
            sim_type = input(
                "\n  [s] - Пошаговая симуляция\n  [d] - Полная симуляция\n\n  Выберите режим: ").lower()
            if sim_type in ["s", "d"]:
                break
            else:
                print("  Неверный ввод! Введите 's' или 'd'")
        if sim_type == "s":
            print("\nЗапущена пошаговая симуляция\n")
            step = 1
            while True:
                key = input(
                    f"\nНажмите Enter для запуска шага #{step} (или 'n' для выхода): ").lower()

                if key != "n":
                    result = casic.sim_step()
                    print_statistics(casic)

                    if result is not None:
                        if result == 0:
                            print("\n" + "="*60)
                            print(" " * 20 + "ГУСИ ПОБЕДИЛИ!")
                            print("="*60)
                        elif result == 1:
                            print("\n" + "="*60)
                            print(" " * 19 + "ИГРОКИ ПОБЕДИЛИ!")
                            print("="*60)
                        break
                    step += 1
                else:
                    print("\nЗавершение программы...\n")
                    break

        elif sim_type == "d":
            print("\nЗапущена полная симуляция\n")
            casic.run_simulation()

        return

    else:
        while True:
            seed = input("ВВЕДИТЕ СИД (ДЛЯ ПРОПУСКА НАЖМИТЕ ENTER): ")

            if seed == "":
                seed = int(time.time()) % 10000
                casic = Casino(seed)
                break
            else:
                try:
                    seed_int = int(seed)
                    casic = Casino(seed_int)
                    seed = seed_int
                    break
                except ValueError:
                    print("ВВЕДЕН НЕВЕРНЫЙ СИД, ПОПРОБУЙТЕ ЕЩЕ РАЗ")
                    continue

        print("\nРЕГИСТРАЦИЯ ИГРОКОВ")
        print("-" * 60)
        
        while True:
            try:
                players_count = int(input("Введите количество игроков: "))
                break
            except ValueError:
                print("Неверный символ, попробуйте еще\n")
                continue


        for i in range(players_count):
            print(f"\nИгрок #{i+1}:")
            
            while True:
                name = input("  Введите имя: ")
                if name != "":
                    break
                else:
                    print("Имя не может быть пустым")
                    continue
            
            while True:
                try:
                    balance = int(input(
                "  Введите баланс (доступные фишки: 5, 10, 25, 100, 200, 500): "))
                    break
                except ValueError:
                    print("Баланс должен быть числом")
                    continue

            casic.player_registry(name, balance)
            print(f"  Игрок {name} зарегистрирован!")

        print("\n" + "="*60)
        print("РЕГИСТРАЦИЯ ГУСЕЙ")
        print("-" * 60)
        
        while True:
            try:        
                gooses_count = int(input("Введите количество гусей: "))
                break
            except ValueError:
                print("Неверный символ, попробуйте еще\n")
                continue

        for i in range(gooses_count):
            print(f"\nГусь #{i+1}:")
            
            while True:  
                name = input("  Введите имя: ")
                if name != "":
                    break
                else:
                    print("Имя не может быть пустым")
                    continue
            
            while True:
                goose_type = input("  Введите тип (WarGoose/HonkGoose/Goose): ")
                if goose_type == "WarGoose" or goose_type == "HonkGoose" or goose_type == "Goose":
                    break
                else:
                    print("Неверный тип гуся, попробуйте еще\n")
                    continue
    

            casic.goose_registry(goose_type, name)
            print(f"  Гусь {name} ({goose_type}) зарегистрирован!")

        main_players = deepcopy(list(casic.player_collection.players.values()))
        main_gooses = deepcopy(list(casic.goose_collection.gooses.values()))

        print("\n" + "="*60)
        print("РЕЖИМ СИМУЛЯЦИИ")
        print("-" * 60)

        while True:
            sim_type = input(
                "\n  [s] - Пошаговая симуляция\n  [d] - Полная симуляция\n\n  Выберите режим: ").lower()
            if sim_type in ["s", "d"]:
                break
            else:
                print("  Неверный ввод! Введите 's' или 'd'")
        if sim_type == "s":
            print("\nЗапущена пошаговая симуляция\n")
            step = 1
            while True:
                key = input(
                    f"\nНажмите Enter для запуска шага #{step} (или 'n' для выхода): ").lower()

                if key != "n":
                    result = casic.sim_step()
                    print_statistics(casic)

                    if result is not None:
                        if result == 0:
                            print("\n" + "="*60)
                            print(" " * 20 + "ГУСИ ПОБЕДИЛИ!")
                            print("="*60)
                        elif result == 1:
                            print("\n" + "="*60)
                            print(" " * 19 + "ИГРОКИ ПОБЕДИЛИ!")
                            print("="*60)
                        break
                    step += 1
                else:
                    print("\nЗавершение программы...\n")
                    break

        elif sim_type == "d":
            print("\nЗапущена полная симуляция\n")
            casic.run_simulation()

        print("\n\nХОТИТЕ СОХРАНИТЬ ИГРУ?")
        ans = input("y/n: ")

        if ans == "y":
            game_name = input("\nВВЕДИТЕ НАЗВАНИЕ СОХРАНЕНИЯ: ")

            save_game(game_name,
                      main_players, main_gooses, int(seed))


if __name__ == "__main__":
    main()
