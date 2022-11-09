#!/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu
from halo import Halo
import json

spinner = Halo(text="Loading", spinner="dots")

spellcheck_url = "https://dictionary.cambridge.org/spellcheck/english/?q="
definition_url = "https://dictionary.cambridge.org/dictionary/english/"
# This is needed to so that you dont get detected as bot
headers = {"User-Agent": "Mozilla/5.0"}


@Halo(text="Loading", spinner="dots")
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


@Halo(text="Loading", spinner="dots")
def get_definitions(word: str) -> list[str]:
    response = requests.get(definition_url + word, headers=headers)

    # If redirection detcted that means, word is not valid
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

        definition = definition.strip()[:-1].capitalize()
        definitions.append(
            {"type": word_type, "definition": definition, "examples": examples}
        )

    return definitions


def main():
    arg = sys.argv[1:][0]
    definitions = get_definitions(arg)

    if len(definitions) == 0:
        suggestions = get_suggestions(arg)

        print(f"No definition found for: \033[1m{arg}\033[0m ❗")
        terminal_menu = TerminalMenu(suggestions, title="Did you mean?")
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) is int:
            arg = suggestions[menu_entry_index]
            definitions = get_definitions(arg)

    print(f"Showig definition for: \033[1m{arg}\033[0m")
    print(json.dumps(definitions, indent=3))


# test words: awesox
if __name__ == "__main__":
    main()
