#!/bin/env python3

import os
import re
import sys
import json
import requests
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu
from halo import Halo
from rich import print
import sqlite3

spinner = Halo(text="Loading", spinner="dots")

# Don't touch this. Unless you want to deal with permission issues in other places
CACHED_DATABASE = os.path.expanduser("~") + "/.cambd-cache.db"
con = sqlite3.connect(CACHED_DATABASE)

SPELLCHECK_URL = "https://dictionary.cambridge.org/spellcheck/english/?q="
DEFINITION_URL = "https://dictionary.cambridge.org/dictionary/english/"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept-Language": "en-US,en;q=0.5",
}


def is_cached(word: str):
    cur = con.execute("SELECT definitions FROM words WHERE word = ?", (word,))
    row = cur.fetchone()
    return json.loads(row[0]) if row else None


def cache_it(word: str, definitions):
    row = word, json.dumps(definitions)
    with con:
        con.execute("INSERT OR REPLACE INTO words VALUES (?, ?)", row)


@spinner
def get_suggestions(word: str):
    page = requests.get(SPELLCHECK_URL + word, headers=REQUEST_HEADERS)
    soup = BeautifulSoup(page.content, "html5lib")
    suggested_words = []

    lis = soup.find_all(attrs={"class": "lbt"})
    for item in lis:
        content = item.find("a", href=True)
        if str(content).__contains__("/search/english"):
            suggested_words.append(content.get_text())

    return suggested_words


def decode_escaped_chars(strg):
    return strg.encode("utf8").decode("utf8", "strict")


@spinner
def get_definitions(word: str):
    # Return cahced version if available
    cached_word = is_cached(word)
    if cached_word is not None:
        return cached_word

    response = requests.get(DEFINITION_URL + word, headers=REQUEST_HEADERS)

    # We are considering a word to be invalid based on redirection only but that may not be the case for valids words
    # with spcaes which we are handling it above statement
    if (
        response.history
        and response.history[0].status_code == 302
        and response.url == "https://dictionary.cambridge.org/dictionary/english/"
    ):
        return []

    soup = BeautifulSoup(response.content, "html5lib")
    definitions = []

    containers = soup.find_all(attrs={"class": "entry-body__el"})
    for div in containers:
        word_type = div.find(attrs={"class": "dpos"})
        word_type = word_type.get_text() if word_type is not None else None

        # no word_type means this definition is past/past-particle form of the word
        # recurs with the original word
        if word_type is None:
            original_word = div.find(attrs={"class": "dx-h"}).get_text()
            return get_definitions(original_word)

        definition = div.find(attrs={"class": "ddef_d"}).get_text()
        example_containers = div.find_all(attrs={"class": "examp"})
        examples = []

        for expl in example_containers:
            example_text = expl.get_text().strip()
            example_text = decode_escaped_chars(example_text)
            examples.append(example_text)

        definition = definition.strip().capitalize()
        definition = definition[:-1] if definition.endswith(":") else definition
        definition = str(re.sub("[ \n]+", " ", definition)) + "."

        if len(examples) > 2:
            examples = examples[:2]

        definition_dict = {
            "Definition": definition,
            "Type": word_type,
            "Examples": examples,
        }
        definitions.append(definition_dict)

    return definitions


def print_definition(word, definition, is_last):
    print(f"\n[bold green]{word}[/] [dim]({definition['Type']})[/]")
    print(definition["Definition"])
    print("\n[dim]Examples:[/]")
    for example in definition["Examples"]:
        print(f"• {example}")
    print("\n=====*=====") if not is_last else print("\n")


def main():
    args = sys.argv[1:]
    searced_word = args[0]

    # handle options
    options = {"show_all": False}
    if len(args) > 1:
        if args[1] == "--show-all":
            options["show_all"] = True

    searched_word_filtered = searced_word.strip().replace(" ", "-").lower()

    # handle db creation
    table = """ CREATE TABLE IF NOT EXISTS words (
    word PRIMARY KEY,
    definitions TEXT
    ); """
    con.execute(table)

    definitions = get_definitions(searched_word_filtered)
    is_from_suggestions = False

    if len(definitions) == 0:
        suggestions = get_suggestions(searched_word_filtered)

        spinner.fail(f"No definition found for: \033[1m{searced_word}\033[0m")
        terminal_menu = TerminalMenu(suggestions, title="Did you mean?")
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) is int:
            suggested_word = suggestions[menu_entry_index]
            definitions = get_definitions(suggested_word)
            searched_word_filtered = suggested_word
            is_from_suggestions = True

    if len(definitions) == 0:
        spinner.warn("No word was selected!")
        return

    # Only show this when the the word was selected from suggestion menu
    if is_from_suggestions:
        spinner.succeed(
            f"Showing definition of \033[1m{searched_word_filtered}\033[0m instead"
        )

    for i in range(len(definitions)):
        if not options["show_all"]:
            print_definition(searched_word_filtered, definitions[0], True)
            break
        is_last = (i + 1) == len(definitions)
        print_definition(searched_word_filtered, definitions[i], is_last)

    cache_it(searched_word_filtered, definitions)


if __name__ == "__main__":
    main()
