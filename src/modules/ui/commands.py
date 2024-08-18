"""User input helper functions"""

import difflib
from enum import Enum
from typing import List, Tuple, Optional


class Command(Enum):
    HELLO = "hello"
    EXIT = "exit"
    CLOSE = "close"
    HELP = "help"
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    SHOW = "show"
    SHOW_ALL = "show-all"
    FIND = "find"
    ADD_PHONE = "add-phone"
    ADD_NOTE = "add-note"
    ADD_TAG = "add-tag"
    REMOVE_TAG = "remove-tag"
    FIND_TAG = "find-tag"
    SORT_TAG = "sort-tag"
    UPCOMING_BIRTHDAY = "upcoming-birthday"
    RESET = "reset"


def get_closest_command(user_input: str) -> Tuple[Optional[Command], List[str]]:
    command_values = [command.value for command in Command]
    words = user_input.lower().split()
    if not words:
        return None, []

    possible_command = words[0]
    if len(words) > 1 and f"{words[0]}-{words[1]}" in command_values:
        possible_command = f"{words[0]}-{words[1]}"
        args = words[2:]
    else:
        args = words[1:]

    closest_matches = difflib.get_close_matches(possible_command, command_values, n=1, cutoff=0.6)

    if closest_matches:
        suggested_command = closest_matches[0]
        if suggested_command != possible_command:
            print(f"Did you mean '{suggested_command}'? Using this command instead.")
        return Command(suggested_command), args
    else:
        print(f"Unknown command '{possible_command}'. Please try again.")
        return None, []
