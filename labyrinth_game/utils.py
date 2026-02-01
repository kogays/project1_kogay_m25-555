import math

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state: dict) -> None:
    """
    Выводит описание текущей комнаты на экран.
    """
    current_room_key = game_state["current_room"]
    room = ROOMS[current_room_key]

    # Название комнаты
    print(f"\n== {current_room_key.upper()} ==")

    # Описание комнаты
    print(room["description"])

    # Предметы в комнате
    items = room.get("items", [])
    if items:
        print("\nЗаметные предметы:")
        for item in items:
            print(f"- {item}")

    # Выходы
    exits = room.get("exits", {})
    if exits:
        exits_list = ", ".join(exits.keys())
        print(f"\nВыходы: {exits_list}")

    # Загадка
    if room.get("puzzle"):
        print("\nКажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    if room["puzzle"] is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]

    alt_answers = {
        "10": ["10", "десять"],
        "шаг шаг шаг": ["шаг шаг шаг", "шаги", "три шага"],
        "12": ["12", "двенадцать"]
    }

    print(question)

    user_answer = input("Ваш ответ: ").strip().lower()

    valid_answers = [a.lower() for a in alt_answers.get(correct_answer,
                                                        [correct_answer])]
    if user_answer in valid_answers:
        print("Верно! Загадка решена 🎉")

        if current_room == "trap_room":
            game_state["player_inventory"].append("trap_key")
            print("Вы нашли особый ключ в ловушке!")
        elif current_room == "library":
            game_state["player_inventory"].append("magic_scroll")
            print("Вы получили древний свиток!")
        elif current_room == "alchemy_lab":
            game_state["player_inventory"].append("elixir")
            print("Вы получили зелье!")
        else:
            game_state["player_inventory"].append("coin")
            print("Вы получили монету!")

        room["puzzle"] = None

    else:
        print("Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    # Проверяем, что мы вообще в комнате с сундуком
    if "treasure_chest" not in room["items"]:
        print("Здесь нет сундука.")
        return

    inventory = game_state["player_inventory"]

    # 1. Проверка ключа
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили! 🏆")
        game_state["game_over"] = True
        return

    # 2. Предложение ввести код
    answer = input(
        "Сундук заперт. У вас нет ключа. Попробовать ввести код? (да/нет): "
    ).strip().lower()

    if answer != "да":
        print("Вы отступаете от сундука.")
        return

    # 3. Проверка кода
    puzzle = room.get("puzzle")
    if puzzle is None:
        print("Похоже, подсказки для взлома нет.")
        return

    _, correct_code = puzzle
    user_code = input("Введите код: ").strip()

    if user_code == correct_code:
        print("Код верный! Замок поддаётся...")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили! 🏆")
        game_state["game_over"] = True
    else:
        print("Неверный код. Сундук остаётся закрытым.")


def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")



def pseudo_random(seed: int, modulo: int) -> int:
    """
    Детерминированный псевдослучайный генератор.
    Возвращает число в диапазоне [0, modulo)
    """
    # 1. Берём синус от seed, умноженного на дробное число
    x = math.sin(seed * 12.9898)

    # 2. "Размазываем" значение
    x = x * 43758.5453

    # 3. Оставляем только дробную часть
    frac = x - math.floor(x)

    # 4. Приводим к диапазону [0, modulo)
    return int(frac * modulo)


def trigger_trap(game_state):
    print("\nЛовушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        idx = pseudo_random(game_state["steps"], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы теряете предмет: {lost_item}")

    else:
        danger = pseudo_random(game_state["steps"], 10)

        if danger < 3:
            print("Ловушка нанесла смертельный удар.")
            print("Вы погибли в лабиринте.")
            game_state["game_over"] = True
        else:
            print("Вы чудом уцелели и выбираетесь из ловушки.")


def random_event(game_state):
    """
    Небольшие случайные события при перемещении игрока
    """

    steps = game_state["steps"]
    current_room = game_state["current_room"]
    inventory = game_state["player_inventory"]

    event_chance = pseudo_random(steps, 10)
    if event_chance != 0:
        return  # ничего не произошло

    event_type = pseudo_random(steps + 1, 3)

    if event_type == 0:
        print("\nВы замечаете что-то блестящее на полу.")
        print("Вы нашли монетку!")

        room_items = ROOMS[current_room]["items"]
        if "coin" not in room_items:
            room_items.append("coin")

    elif event_type == 1:
        print("\nВы слышите странный шорох в темноте...")

        if "sword" in inventory:
            print("Вы сжимаете меч — существо отступает.")

    elif event_type == 2:
        if current_room == "trap_room" and "torch" not in inventory:
            print("\nВ темноте вы не замечаете опасность под ногами!")
            trigger_trap(game_state)