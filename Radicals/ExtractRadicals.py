# File made for use with the Unihan_IRGSources.txt and EquivalentUnifiedIdeograph.txt files (See README.md file for info)
# TODO: Currently the output of this file is not used anywhere...

import numpy as np
import pandas as pd

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"

# %%%%%%%%%%%%%%%%%%%% EXTRACT FROM UNIHAN%%%%%%%%%%%%%%%%%%%%%%


def isradical(radstroke: str) -> tuple[bool, str, str]:
    rad, stroke = radstroke.split(".")
    if stroke == '0' or stroke[0] == "-":
        return True, rad, stroke
    return False, rad, stroke


def removeapostrophe(str: str) -> float:
    rawstring = str.replace("\'", "")
    count = len(str) - len(rawstring)
    return float(str.replace("\'", "")) + float(count*3/10)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%% ADDITIONAL RADICALS%%%%%%%%%%%%%%%%%%%%%%


def removeapostropheagain(str):
    def _removeapostrophe(x):
        rawstring = x.replace("\'", "")
        count = len(x) - len(rawstring)
        return float(x.replace("\'", "")) + float(count*3/10)

    if type(str) != type(""):
        return sum(list(map(_removeapostrophe, str)))/len(str)
    return _removeapostrophe(str)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def __main__():

    ##################### EXTRACT FROM UNIHAN######################

    with open(resources + "Unihan_IRGSources.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
        f.close()

    output = []
    unicodes = []
    strokes = []

    for line in lines:
        if len(line) <= 0:
            continue
        elif line[0] == "#":
            continue

        temp = line.split("	")
        if temp[1] != "kRSUnicode":
            continue

        unicode = temp[0]
        unicodehex = unicode[2:]

        radical_stroke_list = temp[2].split(" ")

        for radstroke in radical_stroke_list:
            israd, rad, stroke = isradical(radstroke)
            if israd:
                if unicode in unicodes:
                    index = unicodes.index(unicode)
                    print("WOW", unicode, chr(int(unicodehex, 16)))
                    if strokes[index] == stroke:
                        print("MEGAWOW", unicode, chr(int(unicodehex, 16)))
                unicodes.append(unicode)
                strokes.append(stroke)
                output.append(unicode + ";" + chr(int(unicodehex, 16)
                                                  ) + ";" + rad + ";" + stroke + "\n")

    outputfile = "".join(output)

    with open(generated + "radicals.txt", "w", encoding="utf-8") as o:
        o.write(outputfile)
        o.close()

    db = pd.read_csv(generated + "radicals.txt", sep=";", header=None)
    db.columns = ["Unicode", "Char", "RadicalCode", "StrokesAfterRadical"]
    db = db.sort_values(by="RadicalCode", key=lambda col: pd.Series([removeapostrophe(
        x)+float(int(db["StrokesAfterRadical"][i])/100)+float(int(db["Unicode"][i][2:], 16)/1000000000) for i, x in enumerate(col)]))
    db = db.set_index("Unicode")
    db.to_csv(generated + "sorted_radicals.txt", sep=";")

    ###############################################################

    ##################### ADDITIONAL RADICALS######################

    with open(resources + "EquivalentUnifiedIdeograph.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
        f.close()

    sortedrads = db.reset_index()
    columns = sortedrads.columns.tolist()
    print(sortedrads)
    og = sortedrads.copy()

    thisisstupidaf = {}

    for line in lines:
        if len(line) <= 0:
            continue
        elif line[0] == "#":
            continue

        new, old = list(map(lambda x: x.split(
            "#")[0].strip(), line.split(";")))
        if "U+"+old not in sortedrads["Unicode"].tolist():
            print("U+"+new, chr(int(new, 16)))
            match new:
                case "2E8B":  # ⺋ 㔾 -> 卩
                    kangxi = "26"
                    strokesafterrad = "0"
                case "2E8E":  # ⺎ 兀 -> 尢 (e.g. 尧)
                    kangxi = "43"
                    strokesafterrad = "0"
                case "2E9B":  # ⺛ 旡 -> 无
                    kangxi = "71"
                    strokesafterrad = "0"
                case "2E9E":  # ⺞ 歺 -> 歹
                    kangxi = "78"
                    strokesafterrad = "1"
                case "2E9F":  # ⺟ 母 -> 毋
                    kangxi = "80"
                    strokesafterrad = "1"
                case "2EA0":  # ⺠ 民 -> 氏
                    kangxi = "83"
                    strokesafterrad = "1"
                # case "2EA9":  # ⺩ 王 -> 玉
                #     kangxi = "96"
                #     strokesafterrad = "-1"
                case "2EB3":  # ⺳ 㓁 -> 网
                    kangxi = "122"
                    strokesafterrad = "-2"
                case "2EB4":  # ⺴    -> 网
                    sortedrads = pd.concat([sortedrads, pd.DataFrame(
                        [["U+"+new, chr(int(new, 16)), "122", "-2"]], columns=columns)], ignore_index=True)
                    continue
                # case "2EB9":  # ⺹ 耂 -> 老
                #     kangxi = "125"
                #     strokesafterrad = "-2"
                # case "2EBA":  # ⺺ 肀 -> 聿
                #     kangxi = "129"
                #     strokesafterrad = "-2"
                case "2EC1":  # ⻁ 虎 -> 虍
                    kangxi = "141"
                    strokesafterrad = "-2"
                # case "31DB":  # [㇛ignored, using𡿨] 巜 -> 巛
                #     print(new, old, "DONT FORGET ME")
                #     sortedrads = pd.concat([sortedrads, pd.DataFrame(
                #         [["U+"+old, chr(int(old, 16)), "47", "0"]], columns=columns)],ignore_index=True)
                #     sortedrads = pd.concat([sortedrads, pd.DataFrame(
                #         [["U+5DDC", chr(int("5DDC", 16)), "47", "-1"]], columns=columns)],ignore_index=True)
                #     continue

            sortedrads = pd.concat([sortedrads, pd.DataFrame(
                [["U+"+new, chr(int(new, 16)), kangxi, strokesafterrad]], columns=columns)], ignore_index=True)
            sortedrads = pd.concat([sortedrads, pd.DataFrame(
                [["U+"+old, chr(int(old, 16)), kangxi, strokesafterrad]], columns=columns)], ignore_index=True)
            del (kangxi)
            del (strokesafterrad)
            continue

        # I have no fucking idea how tf the .iloc[0] does what I want but it does indeed, so wtf
        radcode = sortedrads.loc[sortedrads["Unicode"]
                                 == "U+"+old]["RadicalCode"].iloc[0]
        strokesafterrad = sortedrads.loc[sortedrads["Unicode"]
                                         == "U+"+old]["StrokesAfterRadical"].iloc[0]
        if not ".." in new:
            sortedrads = pd.concat([sortedrads, pd.DataFrame(
                [["U+"+new, chr(int(new, 16)), radcode, strokesafterrad]], columns=columns)], ignore_index=True)
            continue

        newbegin, newend = new.split("..")
        for i in range(int(newbegin, 16), int(newend, 16)+1):
            currhex = hex(i)[2:]
            sortedrads = pd.concat([sortedrads, pd.DataFrame(
                [["U+"+currhex, chr(i), radcode, strokesafterrad]], columns=columns)], ignore_index=True)
            continue

    print(sortedrads)

    sortedrads = sortedrads.sort_values(by="RadicalCode", key=lambda col: pd.Series([removeapostropheagain(
        x)+float(int(sortedrads["StrokesAfterRadical"][i])/100)+float(int(sortedrads["Unicode"][i][2:], 16)/1000000000) for i, x in enumerate(col)]))
    sortedrads = sortedrads.set_index("Unicode")
    sortedrads.to_csv(generated + "sorted_radicals_extra.txt", sep=";")

    ###############################################################


if __name__ == "__main__":
    __main__()
