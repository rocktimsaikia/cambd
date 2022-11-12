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
cached_dictionary = os.path.expanduser("~") + "/.cambd-cache.json"

spellcheck_url = "https://dictionary.cambridge.org/spellcheck/english/?q="
definition_url = "https://dictionary.cambridge.org/dictionary/english/"
headers = {"User-Agent": "Mozilla/5.0"}


@spinner
def get_suggestions(word: str) -> list[str]:
    page = requests.get(spellcheck_url + word, headers=headers)
    soup = BeautifulSoup(page.content, "html5lib")
    suggested_words = []

    lis = soup.find_all(attrs={"class": "lbt"})
    for item in lis:
        content = item.find("a", href=True)
        if str(content).__contains__("/search/english"):
            suggested_words.append(content.get_text())

    return suggested_words


def is_cached(word: str):
    # File exists and has content
    if os.path.exists(cached_dictionary) and os.path.getsize(cached_dictionary) > 0:
        with open(cached_dictionary, "r") as file:
            file_data = json.load(file)
            if word in file_data:
                return file_data[word]


def cache_it(word, definitions):
    # File does not exists or file is empty;
    if not os.path.exists(cached_dictionary) or os.path.getsize(cached_dictionary) == 0:
        with open(cached_dictionary, "w") as ofile:
            json.dump({word: definitions}, ofile)
            return

    # Content already exists, append
    with open(cached_dictionary, "r+") as ofile:
        file_data = json.load(ofile)
        file_data[word] = definitions
        ofile.seek(0)
        json.dump(file_data, ofile)


@spinner
def get_definitions(word: str) -> list[str]:
    # Return cahced version if available
    cached_word = is_cached(word)
    if cached_word is not None:
        return cached_word

    response = requests.get(definition_url + word, headers=headers)

    # We are considering a word to be invalid based on redirection only but that may not be the case for valids words
    # with spcaes which we are handling it above statement
    if response.history and response.history[0].status_code == 302:
        return []

    soup = BeautifulSoup(response.content, "html5lib")
    definitions = []

    containers = soup.find_all(attrs={"class": "entry-body__el"})
    for div in containers:
        word_type = div.find(attrs={"class": "dpos"}).get_text()
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

    spinner.succeed(f"Showing definition for: \033[1m{arg}\033[0m")

    print("\n" + yaml.dump(definitions[0], indent=3, sort_keys=False))
    cache_it(word, definitions)


if __name__ == "__main__":
    main()
