#!/usr/bin/env python3

import click
from halo import Halo
from rich import print
from halo import Halo
from simple_term_menu import TerminalMenu

from cambd import cache
from cambd import dictionary

spinner = Halo(text="Loading", spinner="dots")


def print_definition(word, definition, is_last):
    print(f"\n[bold green]{word}[/] [dim]({definition['Type']})[/]")
    print(definition["Definition"])
    print("\n[dim]Examples:[/]")
    for example in definition["Examples"]:
        print(f"• {example}")
    print("\n=====*=====") if not is_last else print("\n")


def handle_clear_cache(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    cache.cache_clear()
    print("Cleared all the cambd word cache.")
    ctx.exit()


@click.command()
@click.argument("word")
@click.option(
    "-a",
    "--show-all",
    is_flag=True,
    default=False,
    help="Show all the definitions of a word.",
)
@click.option(
    "-c",
    "--clean-cache",
    is_flag=True,
    callback=handle_clear_cache,
    expose_value=False,
    is_eager=True,
    help="Clear all the stored cache from system.",
)
def main(word: str, show_all: bool):
    """Cambridge dictionary CLI app"""

    cache.cache_create()

    # Main
    word_filtered = word.strip().replace(" ", "-").lower()
    definitions = dictionary.get_definitions(word_filtered)
    is_from_suggestions = False

    if len(definitions) == 0:
        suggestions = dictionary.get_suggestions(word_filtered)

        spinner.fail(f"No definition found for: \033[1m{word}\033[0m")
        terminal_menu = TerminalMenu(suggestions, title="Did you mean?")
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) is int:
            suggested_word = suggestions[menu_entry_index]
            definitions = dictionary.get_definitions(suggested_word)
            word_filtered = suggested_word
            is_from_suggestions = True

    if len(definitions) == 0:
        spinner.warn("No word was selected!")
        return

    # Only show this when the the word was selected from suggestion menu
    if is_from_suggestions:
        spinner.succeed(f"Showing definition of \033[1m{word_filtered}\033[0m instead")

    if not show_all:
        print_definition(word_filtered, definitions[0], True)
    else:
        for i in range(len(definitions)):
            is_last = (i + 1) == len(definitions)
            print_definition(word_filtered, definitions[i], is_last)

    cache.cache_append(word_filtered, definitions)


if __name__ == "__main__":
    main()
