# File made for use with the char_v1.0.txt file (See README.md file for info)
# TODO: Currently the output of this file is not used anywhere...

import numpy as np
import pandas as pd
import os

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"

# %%%%%%%%%%%%%%%%%%%% REMOVE PRIVATE CHARS%%%%%%%%%%%%%%%%%%%%%


def isprivate(rawinput: str) -> bool:
    repstr = rawinput.__repr__()
    if len(repstr) < 8:
        return False
    hexstr = repstr[3:-1]
    try:
        n = int(hexstr, 16)
    except Exception as e:
        print("Begin:" + str(len(repstr)) + " " +
              str(len(hexstr)) + repstr + hexstr + str(e))
        return False
    return int("E000", 16) <= n and n <= int("F8FF", 16)


def stripstr(str: str) -> str:
    outputstr = ""
    for char in list(str):
        if not (chr(char) in ["\\", "u", "U"]):
            outputstr += chr(char)
    while outputstr[0] == "0":
        outputstr = outputstr[1:]
    return outputstr


def ischinese(hexstr: str) -> bool:
    n = int(hexstr, 16)
    # should go to 3347F but does not
    return int("2E80", 16) <= n and n <= int("33479", 16)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def __main__():

    ##################### REMOVE PRIVATE CHARS#####################
    with open(resources + "char_v1.0.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
        f.close()

    chars = [((char for char in charss) for charss in list(line))
             for line in lines]
    chars = []
    truelines = []
    for i, line in enumerate(lines):
        for charss in list(line):
            for char in charss:
                chars.append(char)
        tobeappended = "".join(
            list(filter(lambda ch: not isprivate(ch), list(line))))
        if i > 0:
            unicodehex = stripstr(
                tobeappended[0].encode("unicode_escape")).upper()
            if ischinese(unicodehex):
                tobeappended = "U+"+unicodehex + " " + tobeappended
        truelines.append(tobeappended)

    outputfile = "\n".join(truelines)

    with open(generated + "char_v1.0_output.txt", "w", encoding="utf-8") as o:
        o.write(outputfile)
        o.close()
    ###############################################################

    ########################## ONLY DECOMP#########################
    decomps = []

    for i, line in enumerate(truelines):
        if i < 1:
            continue
        temp = line.split(" ")
        unicode = temp[0]
        char = temp[1].split("	")[0]
        temp2 = line.split("DECOMPOSITIONS"+char)
        if len(temp2) > 1:
            decomp = temp2[1].split("TREE")[0].split("MNEMONICS")[0].split(
                "COMPONENTS")[0].replace(";", "&").replace("　", "")
        else:
            print("uni: " + unicode+", char: "+char+", temp2:", temp2)
            decomp = "NULL"
        newline = unicode + ";" + char + ";" + decomp
        decomps.append(newline)

    outputfile = "\n".join(decomps)

    with open(generated + "decomp_output.txt", "w", encoding="utf-8") as o:
        o.write(outputfile)
        o.close()

    db = pd.read_csv(generated + "decomp_output.txt", sep=";", header=None)
    db.columns = ["Unicode", "Char", "Decomposition"]
    db = db.dropna()
    db = db.sort_values(by="Unicode", key=lambda col: pd.Series(
        [int(x[2:], 16) for x in col]))
    db = db.set_index("Unicode")
    db = db.drop_duplicates()

    db.to_csv(generated + "sorted_decomp.txt", sep=";")
    os.remove(generated + "decomp_output.txt")
    ###############################################################
