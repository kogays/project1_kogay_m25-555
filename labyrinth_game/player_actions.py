from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state: dict) -> None:
    """
    Отображает содержимое инвентаря игрока.
    """
    inventory = game_state.get("player_inventory", [])

    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    print("Ваш инвентарь:")
    for item in inventory:
        print(f"- {item}")


def get_input(prompt: str = "> ") -> str:
    """
    Безопасно получает ввод пользователя.
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str) -> None:
    """
    Перемещает игрока в указанном направлении, если выход существует.
    """
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]
    exits = room_data.get("exits", {})

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    if next_room == "treasure_room":
        if "rusty_key" in game_state["player_inventory"]:
            print("Вы используете найденный ключ, "
                  "чтобы открыть путь в комнату сокровищ.")
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps"] += 1

    describe_current_room(game_state)

    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """
    Берет предмет из текущей комнаты и добавляет его в инвентарь игрока.
    """
    current_room_key = game_state["current_room"]
    room = ROOMS[current_room_key]
    items = room.get("items", [])

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in items:
        # Добавляем в инвентарь игрока
        game_state["player_inventory"].append(item_name)

        # Убираем из комнаты
        items.remove(item_name)

        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """
    Использовать предмет из инвентаря.

    :param game_state: словарь состояния игры
    :param item_name: название предмета
    """
    inventory = game_state.get("player_inventory", [])

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы зажгли факел. Стало светлее, и лабиринт виден лучше.")
    elif item_name == "sword":
        print("Вы берёте меч в руки. Чувствуете уверенность и силу.")
    elif item_name == "treasure_key":
        print("Взяв ключ в руки вы понимаете что близки к победе.")
    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Внутри вы нашли ржавый ключ и положили его в инвентарь.")
        else:
            print("Внутри больше ничего нет.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
