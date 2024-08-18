"""Analizing command module"""

import difflib
from typing import List, Tuple

COMMANDS = [
    "hello",
    "exit",
    "close",
    "help",
    "add",
    "edit",
    "delete",
    "show",
    "show-all",
    "find",
    "add-phone",
    "add-note",
    "add-tag",
    "remove-tag",
    "find-tag",
    "sort-tag",
    "upcoming-birthday"
]

def analyze_input(user_input: str) -> Tuple[str, List[str]]:
    words = user_input.lower().split()
    if not words:
        return "", []

    possible_command = words[0]
    if len(words) > 1 and f"{words[0]}-{words[1]}" in COMMANDS:
        possible_command = f"{words[0]}-{words[1]}"
        args = words[2:]
    else:
        args = words[1:]

    closest_matches = difflib.get_close_matches(possible_command, COMMANDS, n=1, cutoff=0.6)

    if closest_matches:
        suggested_command = closest_matches[0]
        if suggested_command != possible_command:
            print(f"Did you mean '{suggested_command}'? Using this command instead.")
        return suggested_command, args
    else:
        print(f"Unknown command '{possible_command}'. Please try again.")
        return "", []