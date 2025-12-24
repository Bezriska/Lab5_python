from src.classes.CasinoClass import Casino



# Первая ошибка RuntimeError
# Поставить точку остановы на 13 строке

# casino = Casino(seed=42)
# casino.player_registry("Player1", 100)
# casino.player_registry("Player2", 150)
# casino.goose_registry("WarGoose", "Goose1", 0) 
# casino.player_collection.players["Player1"].panic_ind = 95
# for player in casino.player_collection.players.values():
#     if player.panic_ind > 92:
#         casino.player_lose(player.name)

# Вторая ошибка при добавлении баланса равного 5 - возвращается пустой список
# Точка остановы на 23 строке

# casino = Casino()
    
# chips_4 = casino.lay_out_for_chips(4)
# chips_5 = casino.lay_out_for_chips(5)
# chips_6 = casino.lay_out_for_chips(6)
# print(f"{chips_4}\n{chips_5}\n{chips_6}")

# Третья ошибка сравнение через is вместо ==
# Поставить точку остановы на 31 строке

# casic = Casino()
# goose_type = ''.join(['W', 'a', 'r', 'G', 'o', 'o', 's', 'e'])
# casic.goose_registry(goose_type, "Goose2", 100)

# Четвертая ошибка неверное логическое условие (игрок с паникой 92 остается в игре, хотя не должен)

# casino = Casino(seed=123)
# casino.player_registry("Player1", 100)
# casino.goose_registry("WarGoose", "Goose1", 0)

# player = casino.player_collection.players["Player1"]

# test_values = [91, 92, 93]
# for panic_value in test_values:
#     player.panic_ind = panic_value
#     should_remove = panic_value >= 92
#     will_remove = panic_value > 92
#     if should_remove != will_remove:
#         print(f"   ОШИБКА: условие > вместо >=")

# Пятая ошибка по умолчанию передан пустой список
# Поставить точку остановы на 57 строке и увидеть, что списки одинаковые

# from src.collections.ChipCollection import ChipCollection
# from src.classes.ChipClass import Chip

# col1 = ChipCollection()
# col2 = ChipCollection()
# col1.add_chip(Chip(10))

# Шестая ошибка неправильно указанное поле
# Поставить точку остановы на 67 строке

# from src.classes.PlayerClass import Player
# from src.classes.ChipClass import Chip
    
# player = Player("TestPlayer")
# player.chips_col.add_chip(Chip(100))
# player.balance
