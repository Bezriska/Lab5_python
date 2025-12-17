
from src.classes.CasinoClass import Casino
import random


def test_error_1_mutating_collection():
    """
    ОШИБКА №1: Изменение коллекции во время итерации
    
    Местоположение: CasinoClass.py, метод sim_step(), строка ~113
    Код: for player in self.player_collection.players.values() БЕЗ list()
    
    Проблема: Внутри цикла вызывается player_lose(), который удаляет игрока
    из словаря во время итерации по нему.
    
    Ожидаемое исключение: RuntimeError: dictionary changed size during iteration
    """
    print("\n\nТЕСТ №1: Изменение коллекции во время итерации")
    
    casino = Casino(seed=42)
    casino.player_registry("Player1", 100)
    casino.player_registry("Player2", 150)
    casino.goose_registry("WarGoose", "Goose1", 0)
    
    casino.player_collection.players["Player1"].panic_ind = 95
    
    print(f"Игроков до: {list(casino.player_collection.players.keys())}")
    print(f"Паника Player1: {casino.player_collection.players['Player1'].panic_ind}")
    
    print("\nЭмуляция ошибки: итерация по словарю с удалением элемента...")
    try:
        for player in casino.player_collection.players.values():
            if player.panic_ind > 92:
                casino.player_lose(player.name)
        print("  Ошибка не воспроизвелась (возможно, Python оптимизировал)")
    except RuntimeError as e:
        print(f"  RuntimeError поймана: {e}")
        print("\nМесто ошибки: CasinoClass.py, строка ~113")
        print("Проблемный код: for player in self.player_collection.players.values()")
        print("Исправление: for player in list(self.player_collection.players.values())")
        print("\nОбъяснение: Нельзя изменять словарь во время итерации по нему.")
        print("Решение: создать копию через list() перед итерацией.")


def test_error_2_off_by_one():
    """
    ОШИБКА №2: Ошибка границы цикла (off-by-one)
    
    Местоположение: CasinoClass.py, метод lay_out_for_chips(), строка ~64
    Код: if value <= 5: ОШИБКА! Исключает значение 5
    
    Проблема: Минимальный номинал фишки 5, но при балансе ровно 5
    метод возвращает пустой список вместо одной фишки.
    
    Ожидаемое поведение: Баланс 5 → пустой список (неправильно)
    """
    print("\n\nТЕСТ №2: Ошибка границы цикла (off-by-one)")
    
    casino = Casino()
    
    chips_4 = casino.lay_out_for_chips(4)
    chips_5 = casino.lay_out_for_chips(5)
    chips_6 = casino.lay_out_for_chips(6)
    
    print(f"Баланс 4 → {len(chips_4)} фишек (ожидается 0): {'OK' if len(chips_4) == 0 else 'ERROR'}")
    print(f"Баланс 5 → {len(chips_5)} фишек (ожидается 1): {'  ОШИБКА!' if len(chips_5) == 0 else 'OK'}")
    print(f"Баланс 6 → {len(chips_6)} фишек (ожидается 1): {'OK' if len(chips_6) == 1 else 'ERROR'}")
    
    if len(chips_5) == 0:
        print("\n  ОШИБКА обнаружена: баланс 5 не конвертируется в фишки!")
        print("Место ошибки: CasinoClass.py, метод lay_out_for_chips(), строка ~64")
        print("Исправление: if value < 5:  или if value < ALLOWED_CHIPS_VALUES[0]:")


def test_error_3_comparison_with_is():
    """
    ОШИБКА №3: Сравнение через is вместо ==
    
    Местоположение: CasinoClass.py, метод goose_registry(), строка ~32-36
    Код: if type is "Goose":  ОШИБКА!
    
    Проблема: Оператор is сравнивает идентичность объектов, а не значения.
    С литералами может работать из-за интернирования, но с динамическими
    строками будет ошибка.
    
    Ожидаемое поведение: TypeError при регистрации гуся с динамической строкой типа
    """
    print("\n\nТЕСТ №3: Сравнение через is вместо ==")
    
    casino = Casino()
    
    print("Тест 1: Литеральная строка")
    try:
        casino.goose_registry("WarGoose", "Goose1", 100)
        print("  Создан с литералом (работает из-за интернирования)")
    except TypeError as e:
        print(f"  Ошибка: {e}")
    
    print("\nТест 2: Строка, гарантированно НЕ интернированная")
    goose_type = ''.join(['W', 'a', 'r', 'G', 'o', 'o', 's', 'e'])
    literal = "WarGoose"
    
    print(f"goose_type = {repr(goose_type)}")
    print(f"literal = {repr(literal)}")
    print(f"id(goose_type) = {id(goose_type)}")
    print(f"id(literal) = {id(literal)}")
    print(f"goose_type == literal: {goose_type == literal}")
    print(f"goose_type is literal: {goose_type is literal}")
    
    if goose_type is not literal:
        print("\n  ОШИБКА обнаружена: is возвращает False, хотя строки равны!")
        print("  Это приведет к TypeError в методе goose_registry()")
        
        try:
            casino.goose_registry(goose_type, "Goose2", 100)
            print("  Гусь НЕ создан (ошибка сработала)")
        except TypeError as e:
            print(f"  TypeError: {e}")
    else:
        print("\n  Python интернировал строку, но концептуально это ошибка!")
    
    print("\nМесто ошибки: CasinoClass.py, метод goose_registry(), строка ~32-36")
    print("Проблемный код: if type is 'Goose':")
    print("Исправление: if type == 'Goose':  использовать == вместо is")
    print("\nПравило: is сравнивает идентичность (id), а == сравнивает значения.")
    print("Используйте is только для None, True, False.")


def test_error_4_wrong_logical_condition():
    """
    ОШИБКА №4: Неверное логическое условие
    
    Местоположение: CasinoClass.py, метод sim_step(), строка ~115
    Код: if player.panic_ind > 92:  ОШИБКА! Пропускает значение 92
    
    Проблема: Граничное значение 92 не обрабатывается, игрок с panic_ind = 92
    не будет удален, хотя должен.
    
    Ожидаемое поведение: Игрок с паникой 92 остается в игре (неправильно!)
    """
    print("\n\nТЕСТ №4: Неверное логическое условие")
    
    casino = Casino(seed=123)
    casino.player_registry("Player1", 100)
    casino.goose_registry("WarGoose", "Goose1", 0)
    
    player = casino.player_collection.players["Player1"]
    
    test_values = [91, 92, 93]
    for panic_value in test_values:
        player.panic_ind = panic_value
        should_remove = panic_value >= 92
        will_remove = panic_value > 92
        
        print(f"\nПаника = {panic_value}:")
        print(f"  Должен быть удален: {should_remove}")
        print(f"  Будет удален (> 92): {will_remove}")
        if should_remove != will_remove:
            print(f"   ОШИБКА: условие > вместо >=")
    
    print("\nМесто ошибки: CasinoClass.py, метод sim_step(), строка ~115")
    print("Исправление: if player.panic_ind >= 92:")


def test_error_5_mutable_default_argument():
    """
    ОШИБКА №5: Использование изменяемого значения по умолчанию
    
    Местоположение: ChipCollection.py, метод __init__(), строка ~6
    Код: def __init__(self, chips=[]):  ОШИБКА!
    
    Проблема: Список [] создается один раз при определении класса и
    используется всеми экземплярами, если не передан аргумент.
    
    Ожидаемое поведение: Два объекта без аргументов разделяют один список!
    """
    print("\n\nТЕСТ №5: Изменяемое значение по умолчанию")
    
    from src.collections.ChipCollection import ChipCollection
    from src.classes.ChipClass import Chip
    
    col1 = ChipCollection()
    col2 = ChipCollection()
    
    print(f"col1.chips id: {id(col1.chips)}")
    print(f"col2.chips id: {id(col2.chips)}")
    
    if id(col1.chips) == id(col2.chips):
        print("  ОШИБКА обнаружена: оба объекта используют ОДИН список")
        
        col1.add_chip(Chip(10))
        print(f"\nДобавили фишку в col1:")
        print(f"  col1 фишек: {len(col1.chips)}")
        print(f"  col2 фишек: {len(col2.chips)}")
        
        if len(col2.chips) > 0:
            print("   col2 тоже изменилась (разделяют список)")
        
        print("\nМесто ошибки: ChipCollection.py, метод __init__(), строка ~6")
        print("Исправление: def __init__(self, chips=None):")
        print("             self.chips = chips if chips is not None else []")
    else:
        print("  Ошибка не воспроизвелась (код исправлен)")


def test_error_6_wrong_attribute_name():
    """
    ОШИБКА №6: Перепутанные поля объекта (неправильное имя атрибута)
    
    Местоположение: PlayerClass.py, метод balance (property), строка ~15
    Код: return self.chips_col.summary_val  ОШИБКА! Должно быть summary_value
    
    Проблема: В ChipCollection атрибут называется summary_value, а не summary_val.
    Это приведет к AttributeError.
    
    Ожидаемое исключение: AttributeError: 'ChipCollection' object has no attribute 'summary_val'
    """
    print("\n\nТЕСТ №6: Неправильное имя атрибута")
    
    from src.classes.PlayerClass import Player
    from src.classes.ChipClass import Chip
    
    player = Player("TestPlayer")
    player.chips_col.add_chip(Chip(100))

    try:
        balance = player.balance
        print(f"  Баланс: {balance}")
        print("  Ошибка не воспроизвелась")
    except AttributeError as e:
        print(f"  AttributeError поймана: {e}")
        print("\nМесто ошибки: PlayerClass.py, метод balance (property), строка ~15")
        print("Проблема: В коде было написано self.chips_col.summary_val")
        print("Исправление: return self.chips_col.summary_value  вместо summary_val")
        print("\nЭта ошибка проявляется при любом обращении к player.balance")
        print("например, при вызове casino.summary_players_balance")


def run_all_tests():
    """Запуск всех тестов ошибок"""
    print("\n\n  ЛАБОРАТОРНАЯ РАБОТА №5: ОТЛАДКА ТИПОВЫХ ОШИБОК")
    print("  Демонстрация ошибок в коде симуляции казино\n\n")
    
    tests = [
        ("Изменение коллекции во время итерации", test_error_1_mutating_collection),
        ("Ошибка границы цикла (off-by-one)", test_error_2_off_by_one),
        ("Сравнение через is вместо ==", test_error_3_comparison_with_is),
        ("Неверное логическое условие", test_error_4_wrong_logical_condition),
        ("Изменяемое значение по умолчанию", test_error_5_mutable_default_argument),
        ("Неправильное имя атрибута", test_error_6_wrong_attribute_name),
    ]
    
    for i, (name, test_func) in enumerate(tests, 1):
        try:
            test_func()
        except Exception as e:
            print(f"\n  Неожиданная ошибка в тесте {i} ({name}):")
            print(f"   {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
    

if __name__ == "__main__":
    run_all_tests()


