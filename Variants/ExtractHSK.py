# File made for use with the charlist.txt file (See README.md file for info)
# TODO: Currently the output of this file is not used anywhere...


import numpy as np
import pandas as pd
import os

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"


def myeval(x):
    if x is np.nan:
        return "NaN"
    # elif type(x) == type([""]):
    #     return "[" + ",".join(x) + "]"

    return x


def __main__():
    print(generated)
    db = pd.read_csv(generated + "commonality_with_variants.txt",
                     sep=";", encoding="utf-8")
    db = pd.read_csv(generated + "commonality_with_variants.txt",
                     sep=";", encoding="utf-8", converters={col: myeval for col in db.columns[2:]})
    db = db.set_index("Unicode")
    dbupdated = db.copy()
    dbupdated["HSK"] = ["NaN"] * len(db)
    print(dbupdated)

    with open(resources + "charlist.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
        f.close()

    chapters = ["一级汉字表", "二级汉字表", "三级汉字表",
                "四级汉字表", "五级汉字表", "六级汉字表", "七一九级汉字表"]
    i = 0
    for line in lines:
        if line == "":
            continue
        elif line[0] == "#":
            continue

        if line in chapters:
            i += 1
            continue
        elif line == "初等手写字表":
            break

        temp = line.split("	")

        if len(temp) < 2:
            raise Exception("Wtf? line was " + line)
        _, char = temp

        unicode = "U+" + hex(ord(char))[2:].upper()

        if unicode not in db.index:
            raise Exception("missing entry! ", unicode, char)

        if dbupdated.loc[unicode]["HSK"] != "NaN":
            raise Exception("WTF DO I DO NOW??", unicode,
                            char, dbupdated.loc[unicode]["HSK"], i)

        dbupdated.loc[unicode, "HSK"] = (str(i) if i < 7 else "A")

    # TODO: make sure the traditional version are given an HSK score as well!

    print(dbupdated)
    dbupdated.to_csv(generated + "hsk_commonality_with_variants_full.txt",
                     sep=";", encoding="utf-8")
    test = dbupdated.loc[dbupdated["HSK"] != "NaN"]
    test.to_csv(generated + "hsk_commonality_with_variants_limited.txt",
                sep=";", encoding="utf-8")


if __name__ == "__main__":
    __main__()
