# cambd

> [Cambridge dictionary](https://dictionary.cambridge.org) cli app

<img src="https://www.dropbox.com/s/1jydlxwzmj8e6po/demo.gif?raw=1" alt="cambd, Cambridge dictionary cli app" />

## Features

- Autosuggest related words on typo.
- Interactive suggestion menu to select words from in the above case.
- Handles past and past-particle words. Returns the original word definition.
- No API/database involved.
- A Persistent caching mechanism. This avoids looking up already searched words; hence fast results.

> Uses python's integrated `sqlite3` for maintaning a persistent cache.

## Installation

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

> By default it caches words in `$HOME/.cambd-cache.db`. To clear the cache if needed <br/> run `cambd --clear-cache`. It is strongly recommended to not modify this file manually.

## LICENSE

[MIT](./LICENSE) License &copy; [Rocktim Saikia](https://rocktimsaikia.com) 2022
