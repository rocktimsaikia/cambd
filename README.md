# cambd-cli

> [Cambridge dictionary](https://dictionary.cambridge.org) cli app for personal use

![cambd demo gif](https://user-images.githubusercontent.com/33410545/202222930-81d79a3c-32b5-4d4a-a999-4dcb8b4fbcfc.gif)

## Why

This is a personal project I have been developing and using for a while. Since English is not my first language. I often had to search the meanings of new words I encounter in podcasts or movies. Personally the only dictionary I use is the [Cambridge dictionary](https://dictionary.cambridge.org/). It has very concise and very easy-to-understand definitions. And I often find myself going back to their site, so I made this CLI tool to automate the process.

## Features

- Autosuggest related words if I mistyped the word when looking it up.
- Interactive suggestion menu to select words from in the above case.
- Handles past and past-particle words. Returns the original word definition.
- No API/database involved.
- Caching mechanism; so that already looked up words does not gets fetched again. Hence fast results.

> Uses python's integreted `sqlite3` for maintaning a locale cache

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
Cambridge dictionary cli app

Usage:
$ cambd <word>

Options:
--show-all	Show all the available definitions of a word. (default is only 1 definition)
--clean-cache	Clean the local cache.
--help		Print this help.

Examples:
$ cambd neccessery
```

> By default it caches words in `$HOME/.cambd-cache.db`. To clear the cache if needed <br/> run `cambd --clear-cache`. It is strongly recommended to not modify this file manually.

## TODO

- [x] Add loading animation.
- [x] Handle error for getting definition of words with spaces.
- [x] Show only 2 examples per definition by default.
- [x] Implement a basic local caching mechanism.
- [x] Handle past/past-participle word definitions.
- [x] Refactor redirection for better word lookup.
- [x] Better/clean way to print the values in terminal.
- [ ] Move the bash port to python too.
- [ ] Create a pypi package out of it.
- [x] Add flag to show all definitions. Default is 1.
- [ ] Show synonyms for the searched word too.

## LICENSE

[MIT](./LICENSE) License &copy; [Rocktim Saikia](https://rocktimsaikia.com) 2022
