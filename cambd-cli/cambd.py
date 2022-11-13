#!/bin/env python3

import os
import re
import sys
import yaml
import json
import requests
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu
from halo import Halo

spinner = Halo(text="Loading", spinner="dots")

# Don't touch this. Unless you want to deal with permission issues in other places
CACHED_DICTIONARY = os.path.expanduser("~") + "/.cambd-cache.json"

SPELLCHECK_URL = "https://dictionary.cambridge.org/spellcheck/english/?q="
DEFINITION_URL = "https://dictionary.cambridge.org/dictionary/english/"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept-Language": "en-US,en;q=0.5",
}


def is_cached(word: str):
    # File exists and has content
    if os.path.exists(CACHED_DICTIONARY) and os.path.getsize(CACHED_DICTIONARY) > 0:
        with open(CACHED_DICTIONARY, "r") as file:
            file_data = json.load(file)
            if word in file_data:
                return file_data[word]


def cache_it(word, definitions):
    # File does not exists or file is empty;
    if not os.path.exists(CACHED_DICTIONARY) or os.path.getsize(CACHED_DICTIONARY) == 0:
        with open(CACHED_DICTIONARY, "w") as ofile:
            json.dump({word: definitions}, ofile)
            return

    # Content already exists, append
    with open(CACHED_DICTIONARY, "r+") as ofile:
        file_data = json.load(ofile)
        file_data[word] = definitions
        ofile.seek(0)
        json.dump(file_data, ofile)


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


@spinner
def get_definitions(word: str):
    # Return cahced version if available
    cached_word = is_cached(word)
    if cached_word is not None:
        return cached_word

    response = requests.get(DEFINITION_URL + word, headers=REQUEST_HEADERS)

    # We are considering a word to be invalid based on redirection only but that may not be the case for valids words
    # with spcaes which we are handling it above statement
    if response.history and response.history[0].status_code == 302:
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
            examples.append(expl.get_text().strip())

        definition = definition.strip().capitalize()
        if definition.endswith(":"):
            definition = definition[:-1]

        if len(examples) > 2:
            examples = examples[:2]

        definition_dict = {
            "Definition": str(re.sub("[ \n]+", " ", definition)) + ".",
            "Type": word_type,
            "Examples": examples,
        }
        definitions.append(definition_dict)

    return definitions


def main():
    arg = sys.argv[1:][0]
    word = arg.strip().replace(" ", "-").lower()
    definitions = get_definitions(word)

    if len(definitions) == 0:
        suggestions = get_suggestions(arg)

        spinner.fail(f"No definition found for: \033[1m{arg}\033[0m")
        terminal_menu = TerminalMenu(suggestions, title="Did you mean?")
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) is int:
            suggested_word = suggestions[menu_entry_index]
            definitions = get_definitions(suggested_word)
            word = suggested_word

    if len(definitions) == 0:
        spinner.warn("No word was selected!")
        return

    spinner.succeed(f"Showing definition for: \033[1m{word}\033[0m")

    print("\n" + yaml.dump(definitions[0], indent=3, sort_keys=False))
    cache_it(word, definitions)


if __name__ == "__main__":
    main()
