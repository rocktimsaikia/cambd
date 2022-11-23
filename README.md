# cambd-cli

> [Cambridge dictionary](https://dictionary.cambridge.org) cli app for personal use

![cambd demo gif](demo.gif)

## Why

This is a personal project I have been developing and using for a while. Since English is not my first language. In general, I often had to search meanings of new words I encounter daily. Personally the only dictionary I use is the [Cambridge dictionary](https://dictionary.cambridge.org/). It has very concise and very easy-to-understand definitions. So I made this CLI tool to automate the process. This tool has become a very convinent part of my daily terminal use, saves me a ton of lookup time in browsers.

## Features

- Autosuggest related words if I mistyped the word when looking it up.
- Interactive suggestion menu to select words from in the above case.
- Handles past and past-particle words. Returns the original word definition.
- No API/database involved.
- A Persistent caching mechanism. This avoids looking up already searched words; hence fast results.

> Uses python's integreted `sqlite3` for maintaning a persistent cache.

## Installation

Make sure you have GNU `make` and `python(v3)` installed on your system.

```sh
# clone the repo
$ git clone https://github.com/rocktimsaikia/cambd-cli.git

# change the working directrory to cambd-cli
$ cd cambd-cli

# install the requirements
$ python3 -m pip install -r requirements.txt

# install cambd-cli
$ sudo make install
```

## Usage

run `cambd --help`

```sh
Usage: cambd [OPTIONS] WORD

  Cambridge dictionary CLI app

Options:
  -a, --show-all     Show all the definitions of a word.
  -c, --clean-cache  Clear all the stored cache from system.
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
