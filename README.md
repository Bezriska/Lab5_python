# Лабораторная работа №5: Отладка кодовой базы проекта на Python

## Цель работы

- Закрепление навыков работы с отладчиком
- Формирование понимания типовых логических и runtime-ошибок
- Освоение методики поиска, анализа и устранения ошибок
- Развитие умения объяснять причину некорректного поведения программы

## Описание

В данной лабораторной работе в код симуляции казино **намеренно внесены 6 типовых ошибок**. Каждая ошибка воспроизводима при запуске тестового файла и должна быть обнаружена с помощью отладчика VS Code.

**ВАЖНО:** Ошибки находятся в исходных файлах проекта. Для их изучения используйте:
- `tests/test_errors_for_lab5.py` — демонстрация ошибок с объяснениями
- `tests/test_debug.py` — отладка ошибок в режиме debug (раскомментируйте нужный блок)

---

## Файлы с ошибками

### src/classes/CasinoClass.py
Содержит ошибки: №1, №2, №3, №4

### src/collections/ChipCollection.py  
Содержит ошибку: №5

### src/classes/PlayerClass.py
Содержит ошибку: №6

---

## Список ошибок (всего 6)

### Ошибка №1: Изменение коллекции во время итерации

**Тип:** Runtime ошибка (RuntimeError)

**Местоположение:** `CasinoClass.py`, метод `sim_step()`, строка ~113

**Проблемный код:**
```python
for player in self.player_collection.players.values():  # ОШИБКА!
    if player.panic_ind > 92:
        self.player_lose(player.name)  # Изменяет словарь во время итерации
```

**Описание:**  
При обработке ставок происходит итерация по словарю игроков (`players.values()`), но внутри цикла может вызываться метод `player_lose()`, который удаляет игрока из этого же словаря. Изменение размера словаря во время итерации приводит к RuntimeError.

**Симптомы:**
```
RuntimeError: dictionary changed size during iteration
```

**Как воспроизвести:**
1. Запустить `python tests/test_errors_for_lab5.py`
2. Тест №1 создаст игрока с высокой паникой (>92)
3. При вызове `sim_step()` игрок будет удален во время итерации
4. Возникнет RuntimeError

**Отладка в VS Code:**
1. Откройте [CasinoClass.py](src/classes/CasinoClass.py#L113)
2. Поставьте breakpoint на строке `for player in ...`
3. Запустите отладку (F5)
4. Пошагово (F10) дойдите до вызова `self.player_lose()`
5. В панели **Variables** наблюдайте за `self.player_collection.players`
6. При входе в `player_lose()` (F11) увидите попытку изменения словаря
7. В **Call Stack** проверьте последовательность вызовов

**Исправление:**
```python
for player in list(self.player_collection.players.values()):
    if player.panic_ind > 92:
        self.player_lose(player.name)
```

Создание копии списка значений через `list()` позволяет безопасно изменять исходный словарь.

---

### Ошибка №2: Ошибка границы цикла (off-by-one)

**Тип:** Логическая ошибка

**Местоположение:** `CasinoClass.py`, метод `lay_out_for_chips()`, строка ~64

**Проблемный код:**
```python
def lay_out_for_chips(self, value):
    chips = []
    value = int(value)
    
    if value <= 5:  # ОШИБКА! Исключает значение 5
        return chips
```

**Описание:**  
Используется условие `if value <= 5`, которое исключает возможность создания фишки при балансе ровно 5. Минимальный номинал фишки равен 5 (`ALLOWED_CHIPS_VALUES[0]`), поэтому баланс 5 должен конвертироваться в одну фишку номиналом 5.

**Симптомы:**
- Баланс 4 → 0 фишек (правильно)
- Баланс 5 → 0 фишек (неправильно, должна быть 1 фишка)
- Баланс 6 → 1 фишка номиналом 5 (правильно)

**Как воспроизвести:**
1. Запустить `python tests/test_errors_for_lab5.py`
2. Тест №2 вызовет `lay_out_for_chips(5)`
3. Метод вернет пустой список вместо `[Chip(5)]`

**Отладка в VS Code:**
1. Откройте [CasinoClass.py](src/classes/CasinoClass.py#L64)
2. Поставьте breakpoint на строке `if value <= 5:`
3. Запустите тест с аргументом value=5
4. В **Debug Console** проверьте:
   - `value <= 5` → True (попадаем в условие)
   - `value < 5` → False (правильное условие)
5. В **Variables** посмотрите `ALLOWED_CHIPS_VALUES[0]` → 5

**Исправление:**
```python
if value < 5:
    return chips

# Или еще лучше:
if value < ALLOWED_CHIPS_VALUES[0]:
    return chips
```

---

### Ошибка №3: Сравнение через `is` вместо `==`

**Тип:** Логическая ошибка

**Описание:**  
Оператор `is` сравнивает идентичность объектов (их адреса в памяти), а не значения. Для сравнения значений строк, чисел и других объектов нужно использовать `==`.

**Проблемный код:**
```python
# Пример ошибки
def goose_registry(self, type: str, name: str, balance: int = 0):
    if type is "Goose":  # ОШИБКА!
        self.goose_collection.add_goose(Goose(name, balance))
```

**Симптомы:**
- Код может работать с литералами благодаря интернированию строк в Python
- Но с динамически созданными строками будет ошибка:
```python
goose_type = "War" + "Goose"  # Динамическая строка
if goose_type is "WarGoose":  # False (хотя значения равны)
    ...  # Код не выполнится
```

**Как воспроизвести:**
```python
type_from_input = "War" + "Goose"
print(type_from_input == "WarGoose")  # True
print(type_from_input is "WarGoose")  # False (ошибка)
```

**Отладка:**
1. Breakpoint на строке сравнения
2. В Variables посмотреть id объектов:
   - `id(type_from_input)` → 4321234567
   - `id("WarGoose")` → 1234567890
3. В Debug Console проверить:
   - `type_from_input == "WarGoose"` → True
   - `type_from_input is "WarGoose"` → False

**Исправление:**
```python
if type == "Goose":
    self.goose_collection.add_goose(Goose(name, balance))
```

**Правило:** Используйте `is` только для сравнения с `None`, `True`, `False`:
```python
if value is None:  # Правильно
if value == None:  # Работает, но не идиоматично
```

---

### Ошибка №4: Неверное логическое условие

**Тип:** Логическая ошибка

**Описание:**  
Использование неправильного оператора сравнения (`>` вместо `>=`, `<` вместо `<=`) приводит к пропуску граничных значений.

**Проблемный код:**
```python
# CasinoClass.py, метод sim_step
if player.panic_ind > 92:  # ОШИБКА! Пропускает значение 92
    player.chips_col.chips = []
    self.player_lose(player.name)
```

**Симптомы:**
- Игрок с `panic_ind = 91` → не удаляется (правильно)
- Игрок с `panic_ind = 92` → не удаляется (неправильно)
- Игрок с `panic_ind = 93` → удаляется (правильно)

**Как воспроизвести:**
```python
casino = Casino()
casino.player_registry("Player1", 100)
player = casino.player_collection.players["Player1"]
player.panic_ind = 92

# Ожидается удаление игрока, но он остается
```

**Отладка:**
1. Breakpoint на строке `if player.panic_ind > 92:`
2. Установить `panic_ind = 92`
3. Пошаговое выполнение (F10)
4. В Debug Console проверить:
   - `player.panic_ind > 92` → False (условие не сработало)
   - `player.panic_ind >= 92` → True (правильное условие)

**Исправление:**
```python
if player.panic_ind >= 92:
    player.chips_col.chips = []
    self.player_lose(player.name)
```

**Аналогичная ошибка в условии победы:**
```python
# Неправильно:
if self.player_collection.summary_balance > 5000:  # Пропускает 5000
    return 1

# Правильно:
if self.player_collection.summary_balance >= 5000:
    return 1
```

---

### Ошибка №5: Использование изменяемого значения по умолчанию

**Тип:** Логическая ошибка (mutable default argument)

**Описание:**  
Если в параметрах функции или метода используется изменяемый объект (список, словарь) как значение по умолчанию, этот объект создается один раз при определении функции и используется повторно при всех вызовах.

**Проблемный код:**
```python
# Пример ошибки
def add_chip(self, chips=[]):  # ОШИБКА! Список общий для всех вызовов
    chips.append(Chip(10))
    return chips
```

**Симптомы:**
```python
result1 = add_chip()  # [Chip(10)]
result2 = add_chip()  # [Chip(10), Chip(10)] - накопление
result3 = add_chip()  # [Chip(10), Chip(10), Chip(10)] - ошибка
```

**Как воспроизвести:**
```python
def buggy_function(items=[]):
    items.append("new_item")
    return items

print(buggy_function())  # ['new_item']
print(buggy_function())  # ['new_item', 'new_item']
print(buggy_function())  # ['new_item', 'new_item', 'new_item']
```

**Отладка:**
1. Breakpoint на строке `def buggy_function(items=[]):`
2. Вызвать функцию несколько раз
3. В Debug Console проверить: `id(items)` - будет одинаковым при всех вызовах!
4. Посмотреть в Variables: список накапливает значения

**Исправление:**
```python
def add_chip(self, chips=None):
    if chips is None:
        chips = []
    chips.append(Chip(10))
    return chips
```


---

### Ошибка №6: Неправильное имя атрибута (перепутанное поле объекта)

**Тип:** Runtime ошибка (AttributeError)

**Местоположение:** `PlayerClass.py`, метод `balance` (property), строка ~15

**Проблемный код:**
```python
@property
def balance(self):
    return self.chips_col.summary_val  # ОШИБКА! Должно быть summary_value
```

**Описание:**  
В классе `Player` свойство `balance` обращается к несуществующему атрибуту `summary_val` объекта `ChipCollection`. Правильное имя атрибута — `summary_value`. Это приводит к AttributeError при любой попытке получить баланс игрока.

**Симптомы:**
```
AttributeError: 'ChipCollection' object has no attribute 'summary_val'. 
Did you mean: 'summary_value'?
```

**Как воспроизвести:**
1. Запустить `python tests/test_errors_for_lab5.py`
2. Тест №6 создаст игрока и попытается получить его баланс
3. При обращении к `player.balance` возникнет AttributeError

```python
from src.classes.PlayerClass import Player
from src.classes.ChipClass import Chip

player = Player("TestPlayer")
player.chips_col.add_chip(Chip(100))

# Попытка получить баланс
balance = player.balance  # AttributeError
```

**Отладка в VS Code:**
1. Откройте [PlayerClass.py](src/classes/PlayerClass.py#L15)
2. Поставьте breakpoint на строке `return self.chips_col.summary_val`
3. Запустите тест
4. Выполните Step Into (F11) на этой строке
5. В **Debug Console** проверьте:
   - `dir(self.chips_col)` → посмотрите доступные атрибуты
   - `hasattr(self.chips_col, 'summary_val')` → False
   - `hasattr(self.chips_col, 'summary_value')` → True
6. В **Variables** изучите объект `self.chips_col`

**Исправление:**
```python
@property
def balance(self):
    return self.chips_col.summary_value
```

**Правило:** Всегда проверяйте правильность имен атрибутов и методов. Используйте автодополнение IDE, чтобы избежать опечаток.

---

## Запуск тестов

### Файлы для тестирования:

#### `tests/test_errors_for_lab5.py`
Демонстрирует все 6 ошибок с подробными объяснениями и выводом в консоль.

**Запуск:**
```bash
python tests/test_errors_for_lab5.py
```

Каждый тест показывает:
- Название и тип ошибки
- Местоположение в коде
- Ожидаемое и фактическое поведение
- Объяснение причины
- Способ исправления

---

#### `tests/test_debug.py`
Файл для отладки в режиме debug VS Code. Содержит закомментированные блоки кода для каждой ошибки.

**Использование:**
1. Откройте файл [tests/test_debug.py](tests/test_debug.py)
2. Раскомментируйте нужный блок ошибки (например, ошибку №1)
3. Поставьте breakpoint (F9) на строке, указанной в комментарии
4. Нажмите F5 (Start Debugging) или выберите "Run > Start Debugging"
5. Используйте инструменты отладчика:
   - **F10** — Step Over (перейти к следующей строке)
   - **F11** — Step Into (войти внутрь функции)
   - **Shift+F11** — Step Out (выйти из функции)
   - **F5** — Continue (продолжить до следующего breakpoint)
6. Наблюдайте за переменными в панели **Variables**
7. Используйте **Debug Console** для проверки выражений
8. Изучите **Call Stack** для понимания последовательности вызовов

**Пример работы с ошибкой №1:**
```python
# В test_debug.py раскомментируйте:
casino = Casino(seed=42)
casino.player_registry("Player1", 100)
casino.player_registry("Player2", 150)
casino.goose_registry("WarGoose", "Goose1", 0) 
casino.player_collection.players["Player1"].panic_ind = 95
for player in casino.player_collection.players.values():  # <- Breakpoint здесь
    if player.panic_ind > 92:
        casino.player_lose(player.name)
```

1. Поставьте breakpoint на строку с `for player in ...`
2. Запустите отладку (F5)
3. В **Variables** посмотрите `casino.player_collection.players` (размер словаря)
4. Нажмите F10 несколько раз, дойдите до `casino.player_lose()`
5. Нажмите F11 чтобы войти в `player_lose()`
6. Увидите строку `del self.player_collection.players[name]`
7. После выхода из функции попытка продолжить итерацию вызовет **RuntimeError**

**Структура файла `test_debug.py`:**
- Ошибка №1: RuntimeError при изменении словаря во время итерации (строка 13)
- Ошибка №2: Off-by-one при балансе 5 (строка 19)
- Ошибка №3: Сравнение `is` vs `==` (строка 31)
- Ошибка №4: Неверное логическое условие >= vs > (строка 36)
- Ошибка №5: Mutable default argument (строка 57)
- Ошибка №6: Неправильное имя атрибута (строка 67)

---


## Выводы

В данной лабораторной работе были рассмотрены 6 типовых ошибок:

1. **Изменение коллекции во время итерации** — RuntimeError при изменении словаря в цикле
2. **Ошибка границы цикла (off-by-one)** — неправильная обработка граничных значений
3. **Сравнение через `is` вместо `==`** — путаница между идентичностью и равенством
4. **Неверное логическое условие** — использование `>` вместо `>=`
5. **Изменяемое значение по умолчанию** — mutable default argument проблема
6. **Неправильное имя атрибута** — опечатка в имени поля объекта

Все ошибки являются логическими или runtime-ошибками, воспроизводимы при запуске и могут быть обнаружены с помощью отладчика VS Code.

**Основные навыки, полученные в ходе работы:**
- Работа с отладчиком VS Code (breakpoints, step execution)
- Использование панели Variables для анализа состояния объектов
- Анализ стека вызовов (Call Stack)
- Проверка выражений в Debug Console
- Понимание типовых паттернов ошибок Python
- Методики поиска и исправления ошибок

**Инструменты отладки:**
- `test_errors_for_lab5.py` — для быстрой демонстрации всех ошибок
- `test_debug.py` — для пошаговой отладки каждой ошибки в VS Code

---

