import sys
import requests
from bs4 import BeautifulSoup

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
        return get_suggestions(word)

    soup = BeautifulSoup(response.content, "html5lib")
    definitions = []

    divs = soup.find_all(attrs={"class": "ddef_d"})
    for div in divs:
        content = div.get_text()
        definitions.append(content)

    return definitions


args = sys.argv[1:]
print(get_definition(args[0]))
