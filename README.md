# `KONSOLDLE`

A clone of the popular word-guessing game Wordle that runs in the terminal. For Linux, Windows and Macintosh

## Options

```
usage: konsoldle [-h] [-a] [-x] [--delay DELAY] [-l WORDS] [-n ANSWERS] [-t GUESSES]

A Wordle for your console.

options:
  -h, --help            show this help message and exit
  -a, --analyser        add the analyser, a row of all found letters
  -x, --hard            enable hard Wordle: you must use all found letters in your guesses
  --delay DELAY         time to show error messages for, in seconds
  -l WORDS, --list WORDS
                        file to pull allowed guesses from
  -n ANSWERS, --answers ANSWERS
                        file to pull a random answer from
  -t GUESSES, --tries GUESSES
                        number of tries

```

## Credits

* To [Reactle](https://github.com/cwackerfuss/react-wordle) for the default lists
* Wordle game for inspiration

# Other things

* You can press `^C` if you want to give up