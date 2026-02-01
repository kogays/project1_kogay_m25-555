#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str) -> None:
    """
    Обрабатывает ввод пользователя и выполняет соответствующую команду.
    """
    command = command.strip().lower()
    if not command:
        return

    parts = command.split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    match cmd:
        case "look":
            describe_current_room(game_state)

        case "inventory" | "inv":
            show_inventory(game_state)

        case "quit" | "exit":
            print("Вы покидаете лабиринт. Игра окончена.")
            game_state["game_over"] = True

        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление. Например: go north")

        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет для использования.")

        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите, что взять. Например: take torch")

        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case direction if direction in {"north", "south", "east", "west"}:
            move_player(game_state, direction)

        case item_name if item_name in ROOMS[
            game_state["current_room"]
        ].get("items", []):
            take_item(game_state, item_name)

        case item_name if item_name in game_state.get("player_inventory", []):
            use_item(game_state, item_name)

        case "help":
            show_help(COMMANDS)

        case _:
            print("Неизвестная команда.")


def main():
    # Инициализация состояния игры
    game_state = {
        "current_room": "entrance",
        "player_inventory": [],
        "steps": 0,
        "game_over": False,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ").strip().lower()
        if not command:
            continue
        process_command(game_state, command)

    print("Спасибо за игру!")


if __name__ == "__main__":
    main()
