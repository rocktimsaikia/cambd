# Cambd

> [Cambridge dictionary](https://dictionary.cambridge.org) cli app

<img src="https://www.dropbox.com/s/1jydlxwzmj8e6po/demo.gif?raw=1" alt="cambd, Cambridge dictionary cli app" />

## Features

- Automatically suggests related words when a typo is detected.
- Provides an interactive suggestion menu for selecting the correct word in case of a typo.
- Supports past and past participle forms, returning the definition of the root word.
- Operates without relying on any external APIs or databases.
- Implements persistent caching to store previously searched words, ensuring faster results. The cache is maintained using Python's built-in `sqlite3`.

## Install

```sh
pip install cambd
```

## Usage

```sh
Usage: cambd [OPTIONS] WORD

Options:
  -a, --show-all         Show all the definitions of a word.
  -d, --dictionary TEXT  Determine which dictionary region to use (uk, us) [default: uk]
  -v, --verbose          Show extra word info ie, word codes & labels. [ex: A2 informal]
  -c, --clear-cache      Clear all the stored cache from system.
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## FAQ

Q. Why scrape instead of using a Dictionary API?

> [!NOTE]
> TBH, As a non native english speaker, I find the cambridge dictionary the most easy to understand. But they don't have any public free API with all the features I want like getting suggestions on misspelled words and give both US and UK definations etc. So I ended up building this cli tool with basic scrapping for my own usecase as I am a terminal power user and don't want to leave the terminal, go to browser, open a new tab just to search for a word meaning.

## LICENSE

[MIT](./LICENSE) License &copy; [Rocktim Saikia](https://rocktimsaikia.dev) 2024
