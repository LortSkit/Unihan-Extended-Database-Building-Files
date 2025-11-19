# File made for use with the JouyouKanjiExcelt.txt and level-1.txt & level-2.txt & level-3.txt files (See README.md file for info)
# TODO: Currently the output of this file is not used anywhere...


import numpy as np
import pandas as pd
import os

datafolder = "../Data/"

filenames = [f"level-{x}.txt" for x in range(1, 3+1)]


def myeval(x):
    if x == "NaN":
        return np.nan

    tempx = x[1:-1]  # removes [ and ]
    return tempx.split(",")


def tounicode(x):
    return "U+"+hex(ord(x))[2:].upper()


def tempeval(x):
    if x == "NaN":
        return "NaN"
    elif x is np.nan:
        return "NaN"

    return x


def getcolvals(db: pd.DataFrame, char: str) -> list[str]:
    def undoeval(x):
        return "NaN" if x is np.nan else "[" + ",".join(x) + "]"
    unicode = tounicode(char)
    allcolumns = db.columns[1:]
    if unicode not in db.index:
        return ["NaN"]*len(allcolumns)
    series = db.loc[unicode]
    allvals = []
    for col in allcolumns:
        val = series[col]
        allvals.append(undoeval(val))

    return allvals


def __main__():
    db = pd.read_csv(datafolder + "variants_extra.txt", sep=";", converters={'CSimplified': myeval, 'CTraditional': myeval,
                                                                             'CSemanticVariant': myeval, 'CContextDependentVariant': myeval, 'CShapeVariant': myeval, 'AMistakenVariant': myeval, 'JSimplified': myeval, 'JTraditional': myeval})
    db = db.set_index("Unicode")
    print(db)

    jouyoudb = pd.read_csv(datafolder + "jouyou.txt", sep=";",
                           converters={'Kyūjitai': myeval})
    jouyoudb = jouyoudb.set_index("Unicode")
    print(jouyoudb)

    alllevels = ["Unicode;Char;CCommonality;TCommonality;JCommonality;CSimplified;CTraditional;CSemanticVariant;CContextDependentVariant;CShapeVariant;AMistakenVariant;JSimplified;JTraditional"]
    jindeces = []
    gradeindeces = []
    i = 1
    for filename in filenames:
        with open(datafolder + filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]
            f.close()
        for line in lines:  # TODO: Also go through their traditional counterparts and add them as well
            if len(line) != 1:
                raise Exception("WTF??" + line + str(len(line)))
            char = line
            variants = getcolvals(db, char)
            tcommonality = "NaN"
            trickyindex = -1
            jcommonality = "NaN"
            ccommonality = "C" + str(i)
            unicode = tounicode(char)
            if unicode in jindeces:
                # Affected characters:
                # U+4E7E 乾 Both map to C1
                # U+85C9 藉 Both map to C1
                # U+77AD 瞭 Both map to C1
                # U+8986 覆 Both map to C1
                # U+5E7A 幺 Now maps ccommonality to C2 and tcommonality to C1
                # U+524B 剋 Now maps ccommonality to C2 and tcommonality to C1
                # U+9EBD 麽 Now maps ccommonality to C2 and tcommonality to C1
                # U+5FB5 徵 Now maps ccommonality to C2 and tcommonality to C1
                # U+5412 吒 Now maps ccommonality to C3 and tcommonality to C2
                # U+82E7 苧 Now maps ccommonality to C3 and tcommonality to C2
                # U+65BC 於 Now maps ccommonality to C3 and tcommonality to C1
                # U+57B5 垵 Now maps ccommonality to C3 and tcommonality to C2
                # U+5925 夥 Now maps ccommonality to C3 and tcommonality to C1
                # U+91D0 釐 Now maps ccommonality to C3 and tcommonality to C1
                trickyindex = jindeces.index(unicode)
                tcommonality = gradeindeces[trickyindex]
                # print("OH SHIT WTF NOWWWWW SIMP", unicode,
                #       char, ccommonality, tcommonality)
                if trickyindex <= 0:
                    raise Exception(f"WTF?? trickyindex was = {trickyindex}")
            jindeces.append(unicode)
            gradeindeces.append(ccommonality)
            if unicode in jouyoudb.index:
                jcommonality = "J" + jouyoudb.loc[unicode]["Grade"]

            newline = unicode + ";"+char + ";" + \
                ccommonality+";" + tcommonality + ";" + \
                jcommonality + ";" + ";".join(variants)
            if trickyindex > -1:
                actualtrickyindex = -1
                for z, stuff in enumerate(alllevels):
                    if unicode in alllevels[z][:10]:
                        actualtrickyindex = z
                alllevels[actualtrickyindex] = newline
            else:
                alllevels.append(newline)

            if unicode in db.index:
                traditionalvariants = db.loc[unicode]["CTraditional"]
                if traditionalvariants is not np.nan:
                    ogchar = char
                    for trad in traditionalvariants:
                        if trad == unicode:
                            continue
                        char = chr(int(trad[2:], 16))
                        ccommonality = "NaN"
                        tcommonality = "C" + str(i)
                        if trad in jindeces:
                            # Affected characters:
                            # U+8457 著 Both map to C1
                            # U+962A 阪 Both map to C2
                            # U+7DDA 線 Now maps ccommonality to C1 instead of C3
                            # U+5641 噁 Now maps ccommonality to C1 instead of C3
                            # U+937E 鍾 Now maps ccommonality to C1 instead of C3
                            # U+860B 蘋 Now maps ccommonality to C1 instead of C3
                            # For the first two, 著 and 阪, are because they are also traditional version of the unicodes we meet in this loop, U+7740 着 and U+5742 坂 respectively,
                            # however they are also considered distinct from those other two in meaning. Doesn't matter here, cuz they get the same grade C2 anyway
                            # For the last four, 線,噁,鍾, and 蘋, they are the traditional counterparts of some uncommon simplifications, U+7F10 缐, U+2BAC7 𫫇, U+953A 锺, U+2C79F 𬞟
                            # 缐 is a variant of 线 (when simplifying 線)
                            # 𫫇 is a variant of 恶 (when simplifying 噁) (e.g., C4H5NO oxazine = (SIMP) 𫫇嗪/恶嗪 vs (TRAD) 噁嗪)
                            # 锺 is a variant of 钟 (when simplifying 鍾)
                            # 𬞟 is a variant of 蘋 (when simplifying 蘋) (no idea why this one isn't used as much? Literally contains 頻=频??)
                            trickyindex = jindeces.index(trad)
                            ccommonality = gradeindeces[trickyindex]
                            # print("OH SHIT WTF NOWWWWW TRAD", "U+"+hex(ord(ogchar))[2:].upper(),
                            #       ogchar, ccommonality + "->" + trad, char, tcommonality)

                        variants = getcolvals(db, char)
                        jcommonality = "NaN"
                        jindeces.append(trad)
                        gradeindeces.append(tcommonality)
                        if trad in jouyoudb.index:
                            jcommonality = "J" + jouyoudb.loc[trad]["Grade"]
                        newline = trad + ";"+char + ";" + \
                            ccommonality+";" + tcommonality + ";" + jcommonality + \
                            ";" + ";".join(variants)
                        alllevels.append(newline)

        i += 1

    for index, row in jouyoudb.iterrows():
        if index in jindeces:
            continue
        char = row["Char"]
        ccommonality = "NaN"
        tcommonality = "NaN"
        jcommonality = "J" + row["Grade"]
        variants = getcolvals(db, char)
        newline = index + ";"+char + ";" + \
            ccommonality+";" + tcommonality + ";" + \
            jcommonality + ";" + ";".join(variants)
        alllevels.append(newline)

    outputfile = "\n".join(alllevels)

    with open(datafolder + "commonality_with_variants_temp.txt", "w", encoding="utf-8") as o:
        o.write(outputfile)
        o.close()

    betteroutput = pd.read_csv(datafolder + "commonality_with_variants_temp.txt", sep=";", converters={'CCommonality': tempeval, 'TCommonality': tempeval, 'JCommonality': tempeval, 'CSimplified': tempeval, 'CTraditional': tempeval,
                                                                                                       'CSemanticVariant': tempeval, 'CContextDependentVariant': tempeval, 'CShapeVariant': tempeval, 'AMistakenVariant': tempeval, 'JSimplified': tempeval, 'JTraditional': tempeval})

    betteroutput = betteroutput.set_index("Unicode")
    betteroutput = betteroutput.sort_values(
        by="Unicode", key=lambda col: pd.Series([int(x[2:], 16) for x in col]))
    betteroutput.to_csv(datafolder + "commonality_with_variants.txt", sep=";")
    os.remove(datafolder + "commonality_with_variants_temp.txt")
