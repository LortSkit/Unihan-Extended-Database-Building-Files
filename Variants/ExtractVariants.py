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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%% JAPANESE%%%%%%%%%%%%%%%%%%%%%%%%%%%


def myeval(x):
    if x == "NaN":
        return np.nan

    tempx = x[1:-1]  # removes [ and ]
    return tempx.split(",")


def undoeval(x):
    return "NaN" if x is np.nan else x
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

    outputfile = "Unicode;Char;CSimplified;CTraditional;CSemanticVariant;CContextDependentVariant;CShapeVariant;AMistakenVariant\n" + \
        "\n".join(output)

    with open(generated + "variants.txt", "w", encoding="utf-8") as o:
        o.write(outputfile)
        o.close()

    db = pd.read_csv(generated + "variants.txt", sep=";")
    db = db.set_index("Unicode")
    print(db)
    ###############################################################

    ########################### JAPANESE###########################

    # Shinjitai;Kyūjitai;Grade
    jouyoudb = pd.read_csv(generated + "jouyou.txt", sep=";",
                           converters={'Kyūjitai': myeval})
    jouyoudb = jouyoudb.set_index("Unicode")
    print(jouyoudb)

    jsimplified = [np.nan]*len(db)
    jtraditional = [np.nan]*len(db)

    for index, row in jouyoudb.iterrows():
        if jouyoudb.loc[index]["Kyūjitai"] is np.nan:
            continue

        if index not in db.index:
            db = pd.concat([db, pd.DataFrame([[index, jouyoudb.loc[index]["Char"], np.nan,
                                               np.nan, np.nan, np.nan, np.nan, np.nan]], columns=["Unicode"]+db.columns.to_list()).set_index("Unicode")])

            jtraditional.append(jouyoudb.loc[index]["Kyūjitai"])
            jsimplified.append(np.nan)
            for kyuujitai in jouyoudb.loc[index]["Kyūjitai"]:
                if kyuujitai in db.index:
                    j = db.index.get_indexer([kyuujitai])[0]
                    if j == -1:
                        raise Exception("WTF??")

                    if jsimplified[j] is np.nan:
                        jsimplified[j] = [index]
                    else:
                        jsimplified[j].append(index)
                else:
                    db = pd.concat([db, pd.DataFrame([[kyuujitai, int(kyuujitai[2:], 16), np.nan,
                                                       np.nan, np.nan, np.nan, np.nan, np.nan]], columns=["Unicode"]+db.columns.to_list()).set_index("Unicode")])
                    jtraditional.append(np.nan)
                    jsimplified.append([index])
        else:
            j = db.index.get_indexer([index])[0]
            if j == -1:
                raise Exception("WTF??")
            if jsimplified[j] is np.nan:
                jtraditional[j] = jouyoudb.loc[index]["Kyūjitai"]
            else:
                jtraditional[j].append(jouyoudb.loc[index]["Kyūjitai"])
            for kyuujitai in jouyoudb.loc[index]["Kyūjitai"]:
                if kyuujitai in db.index:
                    j = db.index.get_indexer([kyuujitai])[0]
                    if j == -1:
                        raise Exception("WTF??")

                    if jsimplified[j] is np.nan:
                        jsimplified[j] = [index]
                    else:
                        jsimplified[j].append(index)
                else:
                    db = pd.concat([db, pd.DataFrame([[kyuujitai, int(kyuujitai[2:], 16), np.nan,
                                                       np.nan, np.nan, np.nan, np.nan, np.nan]], columns=["Unicode"]+db.columns.to_list()).set_index("Unicode")])
                    jtraditional.append(np.nan)
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
