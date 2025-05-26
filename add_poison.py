# Adds junk text in an attempt to make fics unuseable to train AI
# By TricksOfLoki
# Updated 5/26/2025

from io import open
from os.path import exists, isfile
from random import randint
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("filename", type=str, help="input file location")
    parser.add_argument("-m", "--mode", default="default", help="tame or default")
    parser.add_argument("-c", "--class", default="poison", type=str, help="poison class name (default: poison)")

    args = parser.parse_args()
    config = vars(args)

    return config["filename"], config["mode"], config["class"]


def add_poison(filename:str, mode:str, poison_class:str):
    # Check that input file exists
    if not exists(filename) or not isfile(filename):
        print("Invalid file name. Make sure file path is correct")
        quit()

    # Get word list
    with open("popular.txt", mode="r") as file:
        words = file.read()
        words = words.split("\n")
        wordslen = len(words)

    if mode == "tame":
        # Get fic stored in HTML format
        with open(filename, mode="r", encoding="utf-8") as file:
            content = file.read()

        # Add a paragraph of junk text between every regular paragraph
        split = content.split("</p>")
        split.pop(len(split)-1) # Remove final empty itemd
        if len(split) <= 3:
            print("Your text wasn't able to be split into very many paragraphs. You may want to try default mode instead")
        content = ""
        for item in split:
            content += f"{item}</p>\n"
            junk = ""
            for i in range(0, randint(10, 100)):
                junk += words[randint(0, wordslen)] + " "
            content += f"<p class=\"{poison_class}\">{junk}</p>"
        return content

    elif mode == "default":
        # Get fic stored in HTML format
        with open(filename, mode="r", encoding="utf-8") as file:
            content = ""
            next_char = " "
            counting = True
            count = 1

            # Add spans of junk text at random intervals
            while True:
                next_char = file.read(1)
                if not next_char:
                    break
                content += next_char

                if next_char == "<":
                    counting = False
                elif next_char == ">":
                    counting = True

                if counting:
                    count -= 1
                if count <= 0:
                    junk = words[randint(0, wordslen)]
                    content += f"<span class=\"{poison_class}\">{junk}</span>"
                    count = randint(3, 30)
                
        return content
    
    else:
        print("Invalid mode. Try tame or default")
        quit()


if __name__ == "__main__":
    filename, mode, poison_class = parse_args()

    content = add_poison(filename, mode, poison_class)

    # Save new file next to old one
    new_filename = filename.replace(".txt", "_poisoned.txt")
    with open(new_filename, mode="w", encoding="utf-8") as new_file:
        new_file.write(content)
    print(f"Saved to {new_filename}")