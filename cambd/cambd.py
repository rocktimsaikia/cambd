######################################################
#
# cambd - Cambridge dictionary cli app
# written by Rocktim Saikia (saikia.rocktim@proton.me)
#
######################################################

import re
import click
import requests
from halo import Halo
from halo import Halo
from rich import print
from halo import Halo
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu
from .cache import cache_create, cache_clear, cache_append, is_cached
from .__init__ import __version__

spinner = Halo(text="Loading", spinner="dots")

SPELLCHECK_URL = "https://dictionary.cambridge.org/spellcheck/english/?q="
DEFINITION_URL = "https://dictionary.cambridge.org/dictionary/english/"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept-Language": "en-US,en;q=0.5",
}


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
    if cached_word:
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

    dictionaries = soup.find_all(attrs={"class": "dictionary"})
    for dictionary in dictionaries:
        def_blocks = dictionary.find_all(attrs={"class": "ddef_block"})
        dict_region = dictionary.find(attrs={"class": "region"}).get_text().upper()

        for dblock in def_blocks:
            word_type = dblock.find(attrs={"class": "dsense_pos"})
            # use parent's if local not defined
            if word_type == None:
                word_type = dictionary.find(attrs={"class": "dpos"})
            word_type = word_type.get_text() if word_type is not None else None

            # Info about word codes and lables (https://dictionary.cambridge.org/help/codes.html)
            def_info = dblock.find(attrs={"class": "def-info"})
            def_info = def_info.get_text().strip() if def_info is not None else None

            definition = dblock.find(attrs={"class": "ddef_d"})
            if definition:
                definition = dblock.find(attrs={"class": "ddef_d"}).get_text()
                example_containers = dblock.find_all(attrs={"class": "examp"})
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
                    "DictionaryRegion": dict_region,
                    "Info": def_info,
                    "Examples": examples,
                }
                definitions.append(definition_dict)

    return definitions


def print_definition(word, definition, is_last, verbose):
    def_info = " " + definition["Info"] if verbose else ""
    type_info = definition["Type"] if definition["Type"] is not None else "-"
    print(
        f"\n[bold green]{word}[/] [dim]({type_info}) {definition['DictionaryRegion']}{def_info}[/]"
    )
    print(definition["Definition"])
    print("\n[dim]Examples:[/]")
    for example in definition["Examples"]:
        print(f"• {example}")
    print("\n=====*=====") if not is_last else print("\n")


def handle_clear_cache(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    cache_clear()
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
    "-d",
    "--dictionary",
    default="uk",
    show_default=True,
    help="Determine which dictionary region to use (uk, us)",
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    is_flag=True,
    help="Show extra word info ie, word codes & labels. [ex: A2 informal]",
)
@click.option(
    "-c",
    "--clear-cache",
    is_flag=True,
    callback=handle_clear_cache,
    expose_value=False,
    is_eager=True,
    help="Clear all the stored cache from system.",
)
@click.version_option(version=__version__, message="version %(version)s")
def main(word: str, show_all: bool, verbose: bool, dictionary: str):
    cache_create()

    if dictionary not in ["uk", "us"]:
        spinner.warn("Not a valid dictionary region. Available regions are uk, us.")
        return

    # Main
    word_filtered = word.strip().replace(" ", "-").lower()
    definitions = get_definitions(word_filtered)
    is_from_suggestions = False

    if len(definitions) == 0:
        suggestions = get_suggestions(word_filtered)

        spinner.fail(f"No definition found for: \033[1m{word}\033[0m")
        terminal_menu = TerminalMenu(suggestions, title="Did you mean?")
        menu_entry_index = terminal_menu.show()

        if type(menu_entry_index) is int:
            suggested_word = suggestions[menu_entry_index]
            definitions = get_definitions(suggested_word)
            word_filtered = suggested_word
            is_from_suggestions = True

    if len(definitions) == 0:
        spinner.warn("No word was selected!")
        return

    # Only show this when the the word was selected from suggestion menu
    if is_from_suggestions:
        spinner.succeed(f"Showing definition of \033[1m{word_filtered}\033[0m instead")

    wanted_definitions = list(
        filter(
            lambda want: want["DictionaryRegion"].lower() == dictionary.lower(),
            definitions,
        )
    )
    if not show_all:
        print_definition(word_filtered, wanted_definitions[0], True, verbose)
    else:
        for i in range(len(wanted_definitions)):
            is_last = (i + 1) == len(wanted_definitions)
            print_definition(word_filtered, wanted_definitions[i], is_last, verbose)

    cache_append(word_filtered, definitions)
