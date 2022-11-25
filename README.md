# cambd

> [Cambridge dictionary](https://dictionary.cambridge.org) cli app

![cambd demo gif](demo.gif)

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
  -a, --show-all     Show all the definitions of a word.
  -c, --clean-cache  Clear all the stored cache from system.
  --version          Show the version and exit.
  --help             Show this message and exit.
```

> By default it caches words in `$HOME/.cambd-cache.db`. To clear the cache if needed <br/> run `cambd --clear-cache`. It is strongly recommended to not modify this file manually.

## TODO

- [x] Add loading animation.
- [x] Handle error for getting definition of words with spaces.
- [x] Show only 2 examples per definition by default.
- [x] Implement a persistent caching mechanism.
- [x] Handle past/past-participle word definitions.
- [x] Refactor redirection for better word lookup.
- [x] Better/clean way to print the values in terminal.
- [x] Move the bash port to python too.
- [ ] Create a pypi package out of it.
- [x] Add flag to show all definitions. Default is 1.
- [ ] Show synonyms for the searched word too.

## LICENSE

[MIT](./LICENSE) License &copy; [Rocktim Saikia](https://rocktimsaikia.com) 2022
