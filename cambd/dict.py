import re
import requests
from bs4 import BeautifulSoup
from halo import Halo
from cambd import cache

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
    cached_word = cache.is_cached(word)
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
