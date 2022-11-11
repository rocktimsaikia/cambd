# cambd-cli

> Cambridge dictionary cli app for my personal use

https://user-images.githubusercontent.com/33410545/201270253-74791c96-e587-416a-989c-68bd3c09f0bc.mov

## Why

This is a personal project I have been developing and using for a while. The reason is that the only dictionary I use is the [Cambridge dictionary](https://dictionary.cambridge.org/). It has very concise and very easy-to-understand definitions. And I often find myself going back to their site in search of definitions of new words I come across daily, so I made this CLI tool to automate the process.

I only want two things from my CLI

1. I always spell words wrong while typing. In that case suggest me the correct word or related words.
2. If the provided word is spelled correctly then give the defination with minimum examples.

THAT's all!

## Installation

Make sure you have GNU `make` and `python(v3)` installed on your system.

```sh
# Clone the repo
git clone https://github.com/rocktimsaikia/cambd-cli.git
cd cambd-cli

# Install the required dependencies:
make preinstall

# Install the cambd-cli (with sudo)
sudo make install

```

Then you can use it like this:

```sh
cambd neccesseery
```

> The above word spelling is incorrect. So cambd will suggest related words.

## TODO:

- [x] Add loading animation
- [ ] Handle error when there no definations
- [ ] Show only 2 examples per definition by default
- [ ] Add flag to control how many definations to show. Default is 1

## LICENSE

[MIT](./LICENSE) License &copy; [Rocktim Saikia](https://rocktimsaikia.com) 2022
