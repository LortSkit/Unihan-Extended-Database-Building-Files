# While ExtractDecompFromWiktionary.py works as intended,
# it requires that the variants.txt file is created correctly,
# however it wasn't when I first ran the script...
# We have some non-assigned unicode characters to remove as well as
# some scraping that needs to be done for some remaining 288 characters...
# sorry! But it has to be like this now :)


import numpy as np
import pandas as pd
from ExtractDecompFromWiktionary import getDecomp

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"


def undoeval(x):
    return "NaN" if x is np.nan else "[" + ",".join(x) + "]" if type(x) == type([""]) else x


def __main__():

    db = pd.read_csv(generated + "variants.txt", sep=";", encoding="utf-8")
    db = db.set_index("Unicode")
    db = db[["Char"]]
    decomp = pd.read_csv(
        generated + "decomp_scrape_2025-11-24.text", sep=";", encoding="utf-8")
    decomp = decomp.set_index("Unicode")
    decompcharonly = decomp.copy()[["Char"]]

    # decomp[["Unicode"]].isin(db[["Unicode"]])
    # dbunicodes = db["Unicode"].tolist()
    # decompunicodes = decomp["Unicode"].tolist()
    # indices = list(
    #     filter(lambda x: x in dbunicodes, decompunicodes))

    cleaner = decomp[decompcharonly.isin(db).all(axis=1)]
    remainingchars = db[~db.isin(decompcharonly).all(axis=1)]
    for i, (unicode, row) in enumerate(remainingchars.iterrows()):
        char = row["Char"]
        decomp = getDecomp(char)
        print(str(i) + ") Character " + unicode + " " + char +
              " got output: " + decomp.__repr__())
        cleaner = pd.concat([cleaner, pd.DataFrame(
            [[unicode, char, decomp.__repr__().replace("'", "")]], columns=["Unicode", "Char", "Decomposition"]).set_index("Unicode")])
    cleaner = cleaner.sort_values(
        by="Unicode", key=lambda col: pd.Series([int(x[2:], 16) for x in col]))
    cleaner["Decomposition"] = list(
        map(undoeval, cleaner["Decomposition"].tolist()))
    cleaner.to_csv(generated + "decomp_scrape_clean.text",
                   sep=";", encoding="utf-8")


if __name__ == "__main__":
    __main__()
