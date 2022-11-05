#!/bin/env python3

import sys
from types import NoneType
import requests
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu

spellcheck_url = "https://dictionary.cambridge.org/spellcheck/english/?q="
definition_url = "https://dictionary.cambridge.org/dictionary/english/"
headers = {"User-Agent": "Mozilla/5.0"}


def get_suggestions(word):
    page = requests.get(spellcheck_url + word, headers=headers)
    soup = BeautifulSoup(page.content, "html5lib")
    suggested_words = []

    lis = soup.find_all(attrs={"class": "lbt"})
    for item in lis:
        content = item.find("a", href=True)
        if str(content).__contains__("/search/english"):
            suggested_words.append(content.get_text())

    return suggested_words


def get_definition(word):
    response = requests.get(definition_url + word, headers=headers)

    # If redirection detcted that means, word is not valid. So get the suggestions insetad
    if response.history and response.history[0].status_code == 302:
        return

    soup = BeautifulSoup(response.content, "html5lib")
    definitions = []

    divs = soup.find_all(attrs={"class": "ddef_d"})
    for div in divs:
        content = div.get_text()
        definitions.append(content)

    return definitions


def main():
    arg = sys.argv[1:][0]
    definition = get_definition(arg)

    if definition is None:
        suggestions = get_suggestions(arg)
        terminal_menu = TerminalMenu(suggestions)
        menu_entry_index = terminal_menu.show()
        selected_suggestion = suggestions[menu_entry_index]

        final_definition = get_definition(selected_suggestion)
        print(final_definition)


if __name__ == "__main__":
    main()
