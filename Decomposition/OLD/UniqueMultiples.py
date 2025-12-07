import numpy as np
import pandas as pd


datafolder = "../../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"


def myeval(x):
    if x == "NaN":
        return np.nan

    tempx = x[1:-1]  # removes [ and ]
    return tempx.split(", ")


def isinbase(unicode: str) -> bool:
    n = int(unicode[2:], 16)
    return int("3400", 16) <= n <= int("9FFF", 16)


def undoeval(x):
    return "NaN" if x is np.nan else "[" + ",".join(x) + "]" if type(x) == type([""]) else x


def __main__():
    multiples = pd.read_csv(
        generated + "multiples.txt", sep=";", encoding="utf-8", converters={"Decomposition": myeval, "WEqual": myeval})
    multiples = multiples.set_index("Unicode")
    # TODO: Is there any *uncovered* cases within the EquivalentUnifiedIdeograph.txt file?

    counted = []
    count = 0
    trulyunique = []
    for unicode, row in multiples.iterrows():
        if unicode not in counted:
            counted.append(unicode)
            count += 1
            trulyunique.append(unicode)
            for equalunicode in row["WEqual"]:
                counted.append(equalunicode)

    print("Total unique chars in this set: " + str(count))
    uniques = multiples[multiples.index.isin(trulyunique)]

    before = list(filter(isinbase, uniques.index.to_list()))
    print("Before:", len(before))
    for unicode, row in uniques.iterrows():
        if isinbase(unicode):
            continue
        for equalunicode in row["WEqual"]:
            if isinbase(equalunicode):
                uniques = uniques.drop(labels=[unicode])
                uniques = pd.concat(
                    [uniques, multiples.loc[equalunicode].to_frame().T])
                break
    uniques = uniques.reset_index()
    uniques = uniques.sort_values(
        by="index", key=lambda col: pd.Series([int(x[2:], 16) for x in col]))
    uniques = uniques.set_index("index")
    uniques = uniques.rename_axis("Unicode")
    for col in ["Decomposition", "WEqual"]:
        uniques[col] = list(map(undoeval, uniques[col].tolist()))
    uniques.to_csv(generated + "uniques.txt", sep=";", encoding="utf-8")
    print(uniques)
    after = list(filter(isinbase, uniques.index.to_list()))
    print("After:", len(after))

    print(uniques[~uniques.index.isin(after)])
    print("len(multiples)-len(uniques)" + " = " + str(len(multiples)) +
          "-" + str(len(uniques)) + " = " + str(len(multiples)-len(uniques)))


if __name__ == "__main__":
    __main__()
