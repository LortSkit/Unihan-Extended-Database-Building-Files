# File made for use with the Unihan_Variants.txt file (See README.md file for info)

import numpy as np
import pandas as pd

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


def isNextUnicode(smallerunicode: str, biggerunicode: str) -> bool:
    if smallerunicode == "U+4DBE" and biggerunicode == "U+4E00":
        return True
    elif smallerunicode == "U+9FFA" and biggerunicode == "U+FA11":
        return True
    elif smallerunicode == "U+FA18" and biggerunicode == "U+2003E":
        return True
    elif smallerunicode == "U+2F8D2" and biggerunicode == "U+30021":
        return True

    return int(biggerunicode[2:], 16) == int(smallerunicode[2:], 16)+1


def getUnicodesBetween(smallerunicode: str, biggerunicode: str) -> list[str]:
    begin = int(smallerunicode[2:], 16)
    end = int(biggerunicode[2:], 16)
    output = []
    for n in range(begin+1, end):
        output.append("U+"+hex(n)[2:].upper())
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
                    # print(tobeadded)
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
        # print(tobeadded)
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
