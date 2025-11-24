# File made for use with the Unihan_Variants.txt file (See README.md file for info)

import numpy as np
import pandas as pd
import time

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"

# %%%%%%%%%%%%%%%%%%%% EXTRACT FROM UNIHAN%%%%%%%%%%%%%%%%%%%%%%


def makelist(spaceSeperatedUnicodeSourceValues: str) -> list[str]:
    templist = spaceSeperatedUnicodeSourceValues.split(" ")
    return list(map(lambda x: x.split("<")[0], templist))


def makestr(mappings: list[str]) -> str:
    if mappings == []:
        return "NaN"
    return "[" + ",".join(mappings) + "]"


def getBlockNumber(unicode: str) -> int:
    n = int(unicode[2:], 16)
    if n < int("2E80", 16):
        return 0  # Gap
    elif n < int("2E9A", 16):
        return 1  # CJK Radicals Supplement (Part 1)
    elif n == int("2E9A", 16):
        return 2  # Missing
    elif n < int("2EF4", 16):
        return 3  # CJK Radicals Supplement (Part 2)
    elif n < int("2F00", 16):
        return 4  # Missing
    elif n < int("2FD6", 16):
        return 5  # Kangxi Radicals
    elif n < int("2FE0", 16):
        return 6  # Missing
    elif n < int("3400", 16):
        return 7  # Gap
    elif n < int("4DC0", 16):
        return 8  # CJK Unified Ideographs Extension A
    elif n < int("4E00", 16):
        return 9  # Gap
    elif n < int("A000", 16):
        return 10  # CJK Unified Ideographs
    elif n < int("F900", 16):
        return 11  # Gap
    elif n < int("FA6E", 16):
        return 12  # CJK Compatibility Ideographs (Part 1)
    elif n < int("FA70", 16):
        return 13  # Missing
    elif n < int("FADA", 16):
        return 14  # CJK Compatibility Ideographs (Part 2)
    elif n < int("FB00", 16):
        return 15  # Missing
    elif n < int("20000", 16):
        return 16  # Gap
    elif n < int("2A6E0", 16):
        return 17  # CJK Unified Ideographs Extension B
    elif n < int("2A700", 16):
        return 18  # Gap
    elif n < int("2B740", 16):
        return 19  # CJK Unified Ideographs Extension C
    elif n < int("2B81E", 16):
        return 20  # CJK Unified Ideographs Extension D
    elif n < int("2B820", 16):
        return 21  # Missing
    elif n < int("2CEAE", 16):
        return 22  # CJK Unified Ideographs Extension E
    elif n < int("2CEB0", 16):
        return 23  # Missing
    elif n < int("2EBE1", 16):
        return 24  # CJK Unified Ideographs Extension F
    elif n < int("2EBF0", 16):
        return 25  # Missing
    elif n < int("2EE5E", 16):
        return 26  # CJK Unified Ideographs Extension I
    elif n < int("2F800", 16):
        return 27  # Missing
    elif n < int("2FA1E", 16):
        return 28  # CJK Compatibility Ideographs Supplement
    elif n < int("2FA20", 16):
        return 29  # Missing
    elif n < int("30000", 16):
        return 30  # Gap
    elif n < int("3134B", 16):
        return 31  # CJK Unified Ideographs Extension G
    elif n < int("31350", 16):
        return 32  # Missing
    elif n < int("323B0", 16):
        return 33  # CJK Unified Ideographs Extension H
    elif n < int("3347A", 16):
        return 34  # CJK Unified Ideographs Extension J
    elif n < int("33480", 16):
        return 35  # Missing
    else:
        return 36  # Gap


def isNextUnicode(smallerunicode: str, biggerunicode: str) -> bool:
    match smallerunicode, biggerunicode:
        case "U+2E99", "U+2E9B":    # CJK Radicals Supplement - Bridges missing
            return True
        case "U+2EF3", "U+2F00":    # CJK Radicals Supplement - Kangxi Radicals
            return True
        case "U+2FD5", "U+3400":    # Kangxi Radicals - CJK Unified Ideographs Extension A
            return True
        case "U+4DBF", "U+4E00":    # CJK Unified Ideographs Extension A - CJK Unified Ideographs
            return True
        case "U+9FFF", "U+F900":    # CJK Unified Ideographs - CJK Compatibility Ideographs
            return True
        case "U+FA6D", "U+FA70":    # CJK Compatibility Ideographs - Bridges missing
            return True
        case "U+FAD9", "U+20000":   # CJK Compatibility Ideographs - CJK Unified Ideographs Extension B
            return True
        case "U+2A6DF", "U+2A700":  # CJK Unified Ideographs Extension B - CJK Unified Ideographs Extension C
            return True
        case "U+2B73F", "U+2B740":  # CJK Unified Ideographs Extension C - CJK Unified Ideographs Extension D
            return True
        case "U+2B81D", "U+2B820":  # CJK Unified Ideographs Extension D - CJK Unified Ideographs Extension E
            return True
        case "U+2CEAD", "U+2CEB0":  # CJK Unified Ideographs Extension E - CJK Unified Ideographs Extension F
            return True
        case "U+2EBE0", "U+2EBF0":  # CJK Unified Ideographs Extension F - CJK Unified Ideographs Extension I
            return True
        case "U+2EE5D", "U+2F800":  # CJK Unified Ideographs Extension I - CJK Compatibility Ideographs Supplement
            return True
        case "U+2FA1D", "U+30000":  # CJK Compatibility Ideographs Supplement - CJK Unified Ideographs Extension G
            return True
        case "U+3134A", "U+31350":  # CJK Unified Ideographs Extension G - CJK Unified Ideographs Extension H
            return True
        case "U+323AF", "U+323B0":  # CJK Unified Ideographs Extension H - CJK Unified Ideographs Extension J
            return True

    return getBlockNumber(smallerunicode) == getBlockNumber(biggerunicode) and int(biggerunicode[2:], 16) == int(smallerunicode[2:], 16)+1


def getNextUnicode(smallerunicode: str) -> str:
    match smallerunicode:
        case "U+2E99":   # CJK Radicals Supplement - Bridges missing
            return "U+2E9B"
        case "U+2EF3":   # CJK Radicals Supplement - Kangxi Radicals
            return "U+2F00"
        case "U+2FD5":   # Kangxi Radicals - CJK Unified Ideographs Extension A
            return "U+3400"
        case "U+4DBF":   # CJK Unified Ideographs Extension A - CJK Unified Ideographs
            return "U+4E00"
        case "U+9FFF":   # CJK Unified Ideographs - CJK Compatibility Ideographs
            return "U+F900"
        case "U+FA6D":   # CJK Compatibility Ideographs - Bridges missing
            return "U+FA70"
        case "U+FAD9":   # CJK Compatibility Ideographs - CJK Unified Ideographs Extension B
            return "U+20000"
        case "U+2A6DF":  # CJK Unified Ideographs Extension B - CJK Unified Ideographs Extension C
            return "U+2A700"
        case "U+2B73F":  # CJK Unified Ideographs Extension C - CJK Unified Ideographs Extension D
            return "U+2B740"
        case "U+2B81D":  # CJK Unified Ideographs Extension D - CJK Unified Ideographs Extension E
            return "U+2B820"
        case "U+2CEAD":  # CJK Unified Ideographs Extension E - CJK Unified Ideographs Extension F
            return "U+2CEB0"
        case "U+2EBE0":  # CJK Unified Ideographs Extension F - CJK Unified Ideographs Extension I
            return "U+2EBF0"
        case "U+2EE5D":  # CJK Unified Ideographs Extension I - CJK Compatibility Ideographs Supplement
            return "U+2F800"
        case "U+2FA1D":  # CJK Compatibility Ideographs Supplement - CJK Unified Ideographs Extension G
            return "U+30000"
        case "U+3134A":  # CJK Unified Ideographs Extension G - CJK Unified Ideographs Extension H
            return "U+31350"
        case "U+323AF":  # CJK Unified Ideographs Extension H - CJK Unified Ideographs Extension J
            return "U+323B0"

    return "U+"+hex(int(smallerunicode[2:], 16)+1)[2:].upper()


def unicodeGEQ(uni1: str, uni2: str) -> bool:
    n1 = int(uni1[2:], 16)
    n2 = int(uni2[2:], 16)
    return n1 >= n2


def getUnicodesBetween(smallerunicode: str, biggerunicode: str) -> list[str]:
    flag = False
    if smallerunicode == "U+2E7F":
        flag = True
    begin = int(smallerunicode[2:], 16)
    end = int(biggerunicode[2:], 16)
    output = []
    previous = smallerunicode
    n = begin
    while n < end or unicode != biggerunicode:
        n += 1
        unicode = "U+"+hex(n)[2:].upper()
        if not isNextUnicode(previous, unicode):
            unicode = getNextUnicode(previous)
            n = int(unicode[2:], 16)
        if unicodeGEQ(unicode, biggerunicode):
            break
        output.append(unicode)
        previous = unicode
    return output


def basicEval(x):
    return x


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%% JAPANESE%%%%%%%%%%%%%%%%%%%%%%%%%%%


def myeval(x):
    if x == "NaN":
        return "NaN"

    tempx = x[1:-1]  # removes [ and ]
    return tempx.split(",")


def undoeval(x):
    return "NaN" if x is np.nan else "[" + ",".join(x) + "]" if type(x) == type([""]) else x
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def __main__():
    ##################### EXTRACT FROM UNIHAN######################
    with open(resources + "Unihan_Variants.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
        f.close()

    output = []

    CSimplified = []  # kSimplifiedVariant
    CTraditional = []  # kTraditionalVariant
    CSemanticVariant = []  # kSemanticVariant
    CContextDependentVariant = []  # kSpecializedSemanticVariant
    CShapeVariant = []  # kZVariant
    AMistakenVariant = []  # kSpoofingVariant
    # JShinjitai = [] # NOTINUNIHAN! - Likely aren't many that aren't captured by simp/trad relation
    # JKyuujitai = [] # NOTINUNIHAN! - Likely aren't many that aren't captured by simp/trad relation

    currentunicode = "U+3400"
    for line in lines:
        if len(line) <= 0:
            continue
        elif line[0] == "#":
            continue

        temp = line.split("	")
        unicode = temp[0]
        if unicode != currentunicode:
            output.append(currentunicode + ";" + chr(int(currentunicode[2:], 16)) + ";" + makestr(CSimplified) + ";" + makestr(CTraditional) + ";" + makestr(
                CSemanticVariant) + ";" + makestr(CContextDependentVariant) + ";" + makestr(CShapeVariant) + ";" + makestr(AMistakenVariant))

            CSimplified = []               # kSimplifiedVariant
            CTraditional = []              # kTraditionalVariant
            CSemanticVariant = []          # kSemanticVariant
            CContextDependentVariant = []  # kSpecializedSemanticVariant
            CShapeVariant = []             # kZVariant
            AMistakenVariant = []          # kSpoofingVariant
            if not isNextUnicode(currentunicode, unicode):
                for unicodeinbetween in getUnicodesBetween(currentunicode, unicode):
                    tobeadded = unicodeinbetween + ";" + \
                        chr(int(unicodeinbetween[2:], 16)
                            ) + ";NaN;NaN;NaN;NaN;NaN;NaN"
                    output.append(tobeadded)

            currentunicode = unicode

        keyword = temp[1]
        mappings = makelist(temp[2])

        match keyword:
            case "kSimplifiedVariant":
                if CSimplified != []:
                    CSimplified.append(mappings)
                else:
                    CSimplified = mappings
            case "kTraditionalVariant":
                if CTraditional != []:
                    CTraditional.append(mappings)
                else:
                    CTraditional = mappings
            case "kSemanticVariant":
                if CSemanticVariant != []:
                    CSemanticVariant.append(mappings)
                else:
                    CSemanticVariant = mappings
            case "kSpecializedSemanticVariant":
                if CContextDependentVariant != []:
                    CContextDependentVariant.append(mappings)
                else:
                    CContextDependentVariant = mappings
            case "kZVariant":
                if CShapeVariant != []:
                    CShapeVariant.append(mappings)
                else:
                    CShapeVariant = mappings
            case "kSpoofingVariant":
                if AMistakenVariant != []:
                    AMistakenVariant.append(mappings)
                else:
                    AMistakenVariant = mappings
    output.append(currentunicode + ";" + chr(int(currentunicode[2:], 16)) + ";" + makestr(CSimplified) + ";" + makestr(CTraditional) + ";" + makestr(
        CSemanticVariant) + ";" + makestr(CContextDependentVariant) + ";" + makestr(CShapeVariant) + ";" + makestr(AMistakenVariant))
    unicode = "U+3347A"
    for unicodeinbetween in getUnicodesBetween(currentunicode, unicode):
        tobeadded = unicodeinbetween + ";" + \
            chr(int(unicodeinbetween[2:], 16)
                ) + ";NaN;NaN;NaN;NaN;NaN;NaN"
        output.append(tobeadded)

    for unicodeinbetween in getUnicodesBetween("U+2E7F", "U+2EF4"):
        tobeadded = unicodeinbetween + ";" + \
            chr(int(unicodeinbetween[2:], 16)
                ) + ";NaN;NaN;NaN;NaN;NaN;NaN"
        output.append(tobeadded)

    outputfile = "Unicode;Char;CSimplified;CTraditional;CSemanticVariant;CContextDependentVariant;CShapeVariant;AMistakenVariant\n" + \
        "\n".join(output)

    with open(generated + "variants_temp.txt", "w", encoding="utf-8") as o:
        o.write(outputfile)
        o.close()

    db = pd.read_csv(generated + "variants_temp.txt", sep=";")
    db = pd.read_csv(generated + "variants_temp.txt", sep=";",
                     converters={col: basicEval for col in db.columns})
    db = db.set_index("Unicode")
    db = db.sort_values(
        by="Unicode", key=lambda col: pd.Series([int(x[2:], 16) for x in col]))
    db.to_csv(generated + "variants.txt", sep=";")
    print(db)
    ###############################################################

    ########################### JAPANESE###########################

    # Shinjitai;Kyūjitai;Grade
    jouyoudb = pd.read_csv(generated + "jouyou.txt",
                           sep=";", converters={'Kyūjitai': myeval})
    jouyoudb = jouyoudb.set_index("Unicode")
    print(jouyoudb)

    jsimplified = ["NaN"]*len(db)
    jtraditional = ["NaN"]*len(db)

    for index, row in jouyoudb.iterrows():
        if jouyoudb.loc[index]["Kyūjitai"] == "NaN":
            continue

        if index not in db.index:
            db = pd.concat([db, pd.DataFrame([[index, jouyoudb.loc[index]["Char"], "NaN",
                                               "NaN", "NaN", "NaN", "NaN", "NaN"]], columns=["Unicode"]+db.columns.to_list()).set_index("Unicode")])

            jtraditional.append(jouyoudb.loc[index]["Kyūjitai"])
            jsimplified.append("NaN")
            for kyuujitai in jouyoudb.loc[index]["Kyūjitai"]:
                if kyuujitai in db.index:
                    j = db.index.get_indexer([kyuujitai])[0]
                    if j == -1:
                        raise Exception("WTF??")

                    if jsimplified[j] == "NaN":
                        jsimplified[j] = [index]
                    else:
                        jsimplified[j].append(index)
                else:
                    db = pd.concat([db, pd.DataFrame([[kyuujitai, int(kyuujitai[2:], 16), "NaN",
                                                       "NaN", "NaN", "NaN", "NaN", "NaN"]], columns=["Unicode"]+db.columns.to_list()).set_index("Unicode")])
                    jtraditional.append("NaN")
                    jsimplified.append([index])
        else:
            j = db.index.get_indexer([index])[0]
            if j == -1:
                raise Exception("WTF??")
            if jsimplified[j] == "NaN":
                jtraditional[j] = jouyoudb.loc[index]["Kyūjitai"]
            else:
                jtraditional[j].append(jouyoudb.loc[index]["Kyūjitai"])
            for kyuujitai in jouyoudb.loc[index]["Kyūjitai"]:
                if kyuujitai in db.index:
                    j = db.index.get_indexer([kyuujitai])[0]
                    if j == -1:
                        raise Exception("WTF??")

                    if jsimplified[j] == "NaN":
                        jsimplified[j] = [index]
                    else:
                        jsimplified[j].append(index)
                else:
                    db = pd.concat([db, pd.DataFrame([[kyuujitai, int(kyuujitai[2:], 16), "NaN",
                                                       "NaN", "NaN", "NaN", "NaN", "NaN"]], columns=["Unicode"]+db.columns.to_list()).set_index("Unicode")])
                    jtraditional.append("NaN")
                    jsimplified.append([index])

    db["JSimplified"] = jsimplified
    db["JTraditional"] = jtraditional
    db = db.sort_values(
        by="Unicode", key=lambda col: pd.Series([int(x[2:], 16) for x in col]))
    print(db)
    # test with Shibuya (渋谷)'s first character 渋 (should map to 澁)
    print(chr(int(db.loc["U+6E0B"]["JTraditional"][0][2:], 16)))

    dboutput = db.copy()
    for col in db.columns.to_list()[1:]:

        dboutput[col] = list(map(undoeval, dboutput[col].tolist()))
    dboutput.to_csv(generated+"variants_extra.txt", sep=";")
    print(dboutput)

    ###############################################################


if __name__ == "__main__":
    __main__()
