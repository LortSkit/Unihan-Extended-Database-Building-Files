import requests
import numpy as np
import pandas as pd
import re
import os

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"


def isChineseChar(char: str) -> bool:
    n = ord(char)
    # rough estimate & U+25C7 ◇ occurs in 𠄷's decomposition
    return (int("2E80", 16) <= n and n <= int("33479", 16)) or (n == int("25C7", 16))


# def isChineseStr(str: str) -> bool:
#     for char in str:
#         if isChineseChar(char):
#             return True
#     return False


def chineseOnly(str: str) -> str:
    output = ""
    for char in str:
        if isChineseChar(char):
            output += char

    return output


# def isStrokeChar(char: str) -> bool:
#     n = ord(char)
#     # hanzi U+4E00 一 is not the same as stroke U+31D0 ㇐
#     return (int("31C0", 16) <= n and n <= int("31E5", 16))


# def isCompositionChar(char: str) -> bool:
#     n = ord(char)
#     return (int("2FF0", 16) <= n and n <= int("2FFF", 16)) or (n == int("303E", 16)) or (n == int("31EF", 16))


# def containsStrokes(str: str) -> bool:
#     for char in str:
#         if isStrokeChar(char):
#             return True
#     return False


def unicodeLessThanEqualTo(uni1, uni2):
    return int(uni1[2:], 16) <= int(uni2[2:], 16)


def getDecomp(char: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(
        "https://en.wiktionary.org/wiki/"+char, headers=headers)
    response.raise_for_status()
    response.encoding = "utf-8"
    text = response.text[:100000][-70000:]
    if "Wiktionary does not yet have an entry for" in text:
        print("Character U+" + hex(ord(char))
              [2:].upper() + " " + char + " does not have an entry on Wiktionary")
        return "NaN"
    elif "composition" not in text:
        print("Character U+" + hex(ord(char))
              [2:].upper() + " " + char + " does not have any composition data on Wiktionary")
        return "NaN"
    split = re.sub(r"\([^)]*\)", r"", text.split(
        ">composition")[1][:2100]).split(")")[0]
    almost = split.split("</a></span>)")[0]
    temp = almost.split("or")
    output = []
    for togetdecomp in temp:
        newsplit = togetdecomp.split(">")
        outputlist = list(map(lambda x: x.split("<")[0], newsplit))
        output.append(chineseOnly("".join(outputlist)))
    return output


lastrecord = "U+575B"

db = pd.read_csv(
    generated + "variants.txt", sep=";", encoding="utf-8")
db = db[["Unicode", "Char"]]
db = db.set_index("Unicode")
db = db.loc[lastrecord:]
print(db)


# will delete contents of existing file
if lastrecord is None:
    with open(generated + "decomp_scrape.txt", "w", encoding="utf-8") as f:
        f.write("Unicode;Char;Decomposition\n")
        f.close()

# will delete contents of existing file
print("Begin webscrape starting with char " +
      ("U+3400 㐀" if lastrecord is None else lastrecord + " " + chr(int(lastrecord[2:], 16))))
for i, (unicode, row) in enumerate(db.iterrows()):
    if i == 0 and lastrecord is not None:
        continue
    char = row["Char"]
    decomp = getDecomp(char)
    with open(generated + "decomp_scrape.txt", "a", encoding="utf-8") as f:
        f.write(unicode + ";" + char + ";" +
                decomp.__repr__().replace("'", "") + "\n")
        f.close()

# difficultChar = ["𰻝", "㒪", "㚓", "刃", "劣", "𠄷"]
# for i, char in enumerate(difficultChar):
#     unicode = "U+" + hex(ord(char))[2:].upper()
#     decomp = getDecomp(char)

#     # will delete contents of existing file
#     with open(generated + "decomp_scrape.txt", "a", encoding="utf-8") as f:
#         f.write(unicode + ";" + char + ";" +
#                 decomp.__repr__().replace("'", "") + "\n")
#         f.close()
