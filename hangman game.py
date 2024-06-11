__author__ = "Konrad Ceglarski"

from os import system
import string
import random
import codecs
import msvcrt

# variables
abc = string.ascii_lowercase + "ąćęłńóśżź"
used = []
words = []
word = ""

stages = []
stage = 0
points = 0

playing = True

#setup
def var_reset():
    global used, word, stage, points
    used = []
    word = random.choice(words)
    stage = 0
    points = 0

# get data
def get_data():
    with open("hangman stages.txt", "r") as f:
        data = f.readlines()
        helper = ""
        for i, l in enumerate(data):
            if l != '\n' or i == len(data)-1:
                helper += l
            if l == '\n' or i == len(data)-1:
                helper = helper[0:-1] if helper[-1] == '\n' else helper
                stages.append(helper)
                helper = ""
    with codecs.open("hangman words.txt", "r", encoding="852") as f:
        data = f.readlines()
        for l in data:
            for elem in l.split():
                words.append(elem)

# some display functions
def displayed_word(word, used):
    return "".join([ch if ch in used else "*" for ch in word])

def check_points(word, used):
    return len([ch for ch in word if ch in used])

def wrong(word, used):
    return ", ".join([ch for ch in used if ch not in word])

def correct(word, used):
    return ", ".join([ch for ch in used if ch in word])

def check_correct(word, used):
    global stage
    if used[-1] not in word:
        stage += 1

# input letter function
def special_input():
    global playing
    ch = msvcrt.getch().lower()
    ch_encoded = codecs.decode(ch, encoding="852")
    if ch == b'\x1b':
        print('esc')
        playing = False
    elif ch_encoded in abc and ch_encoded not in used:
        print(ch_encoded)
        used.append(ch_encoded)
    else:
        special_input()

# display
def display():
    system("cls")

    print(f"Your word has {len(word)} letters\nand it looks like this:")
    system(f"echo \033[97m{displayed_word(word, used)}\033[0m")

    print(f"\n{stages[stage]}\n")

    system(f"echo Your points so far: \033[93m{points}\033[0m")
    system(f"echo You've entered (wrong): \033[91m{wrong(word, used)}\033[0m")
    system(f"echo You've entered (correct): \033[92m{correct(word, used)}\033[0m")

    print("\n> Choose a letter: ", end="")

# main
def main():
    global points
    while playing:
        if points != len(word)-1:
            if stage != len(stages)-1:
                points = check_points(word, used)
                display()
                special_input()
                if playing:
                    check_correct(word, used)
                    system("pause")
            else:
                system("cls")
                print(f"Your word has {len(word)} letters\nand it looks like this:")
                system(f"echo \033[97m{displayed_word(word, used)}\033[0m")
                print(f"\n{stages[stage]}\n")
                system("echo \033[91mYou have lost!\033[0m")
                system(f"echo The word was: \033[97m{word}\033[0m")
                system("pause")
                var_reset()
        elif points == len(word)-1:
            system("cls")
            system("echo \033[92mYou have won!\033[0m")
            system(f"echo The word was: \033[97m{word}\033[0m")
            system("pause")
            var_reset()
    
# setup
get_data()
var_reset()
main()

print("Closing...")
system("pause")