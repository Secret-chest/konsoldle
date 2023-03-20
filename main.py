#!/usr/bin/python3

__version__ = "v0.1"

from termcolor import colored as col
import colorama
from random import choice
import time
import argparse

colorama.init()

konsoldleLogo = col("K", "light_yellow", attrs=["bold"]) + col("O", "light_grey", attrs=["bold"]) + col("N", "light_green", attrs=["bold"]) + col("S", "light_green", attrs=["bold"]) + col("O", "light_grey", attrs=["bold"]) + col("L", "light_yellow", attrs=["bold"]) + col("D", "light_green", attrs=["bold"]) + col("L", "light_green", attrs=["bold"]) + col("E", "light_grey", attrs=["bold"])


parser = argparse.ArgumentParser(prog="konsoldle", description="A Wordle for your console.")
parser.add_argument("-a", "--analyser", dest="analyser", action="store_true", help="add the analyser, a row of all found letters")
parser.add_argument("-p", "--placeholder", dest="placeholder", action="store_true", help="add a word placeholder")
parser.add_argument("-x", "--hard", dest="hard", action="store_true", help="enable hard Wordle: you must use all found letters in your guesses")
parser.add_argument("--delay", dest="delay", type=float, default=1, help="time to show error messages for, in seconds")
parser.add_argument("-l", "--list", dest="words", default="./guesses.txt", help="file to pull allowed guesses from")
parser.add_argument("-n", "--answers", dest="answers", default="./answers.txt", help="file to pull a random answer from")
parser.add_argument("-t", "--tries", dest="guesses", type=int, default=6, help="number of tries")
args = parser.parse_args()
analyser = args.analyser
placeholder = args.placeholder
hard = args.hard
errorDelay = args.delay
guesses = args.guesses
with open(args.words) as file:
    words = [line.rstrip().upper() for line in file]
with open(args.answers) as file:
    answers = [line.rstrip().upper() for line in file]
word = choice(answers)


def clearLines(n=1):
    up = '\033[1A'
    clear = '\x1b[2K'
    for i in range(n):
        print(up, end=clear)


def getPlaced(letter):
    return col("[" + letter + "]", "white", "on_green", attrs=["bold"])


def getFound(letter):
    return col("(" + letter + ")", "white", "on_yellow")


def getBad(letter):
    return col(" " + letter + " ", "white", "on_grey")


placed = {}
found = set()
bad = set()


def getWord(guess):
    global word, placed, found, bad
    ci = 0
    formatted = ""
    correct = True

    for c in guess:
        if c == word[ci]:
            formatted += getPlaced(c)
            placed[c] = ci
        elif c in word:
            formatted += getFound(c)
            correct = False
            found.add(c)
        else:
            formatted += getBad(c)
            correct = False
            bad.add(c)
        ci += 1
    return formatted, correct


def getPlaceholder():
    global word
    placeholder = col(len(word) * "[ ]", "light_grey", "on_grey", attrs=["dark"])
    return placeholder


# Information
print(f"{ konsoldleLogo } {__version__} ({ col('konsoldle --help', 'light_blue') } for more information)")

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(f"Guess a {len(word)}-letter word")
print(f"{ getPlaced(choice(alphabet)) } - letter is in the word and at the correct position")
print(f"{ getFound(choice(alphabet)) } - letter appears in the word, but at another position")
print(f"{ getBad(choice(alphabet)) } - letter isn't anywhere in the word")


# Game
i = 1
while i <= guesses:
    if placeholder:
        print(getPlaceholder())
    try:
        guess = input(f"Your Guess ({i}/{guesses}) > ").upper()
    except KeyboardInterrupt:
        try:
            print()
            clearLines()
            giveup = input(f"{ col('Give up?', 'light_red') } (y/n/^C) > ").upper()
            if giveup == "Y" or giveup == "YES":
                clearLines(1 + placeholder)
                print(f"{ col('Game Over:', 'light_red', attrs=['bold']) } You gave up at guess {i}/{guesses}.")
                break
            else:
                clearLines(1 + placeholder)
                continue
        except KeyboardInterrupt:
            print()
            exit()

    if hard:
        invalid = False
        for c in found:
            if c not in guess:
                invalid = True
        for c in placed.keys():
            if c != guess[placed[c]]:
                invalid = True
        if invalid:
            print(f"{ col('Error:', 'light_red', attrs=['bold']) } Hard Mode: Please use all revealed hints")
            time.sleep(errorDelay)
            clearLines(2)
            continue
    if guess not in words or len(guess) != len(word):
        if not guess:
            clearLines()
            continue
        else:
            print(f"{ col('Error:', 'light_red', attrs=['bold']) } Invalid word")
            try:
                time.sleep(errorDelay)
                clearLines(2 + placeholder)
                continue
            except KeyboardInterrupt:
                print()
                clearLines(3 + placeholder)
                continue
    else:
        clearLines(1 + (analyser if i > 1 else 0) + placeholder)
    formatted, correct = getWord(guess)
    print(str(i) + ". " + formatted)
    if analyser:
        print("Letters:", end=" ")
        for c in placed.keys():
            print(getPlaced(c), end="")
        for c in found:
            print(getFound(c), end="")
        for c in bad:
            print(getBad(c), end="")
        print()
    if correct:
        print(f"{ col('Game Over:', 'light_green', attrs=['bold']) } You guessed the word in {i} tries.")
        break
    if i == guesses and not correct:
        print(f"{ col('Game Over:', 'light_red', attrs=['bold']) }: You lost.")
    i += 1
print(f"The word was { col(word, color='light_green', attrs=['underline']) }")
