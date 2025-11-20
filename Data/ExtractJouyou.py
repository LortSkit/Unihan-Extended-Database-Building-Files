# File made for use with the JouyouKanjiExcel.txt file (See README.md file for info)

import numpy as np
import pandas as pd


def jouyoueval(x):
    if x == "":
        return np.nan

    return list(x)


datafolder = "./"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"


def __main__():

    # Shinjitai;Kyūjitai;Grade
    jouyoudb = pd.read_csv(resources + "./JouyouKanjiExcel.txt",
                           # no idea why it's utf-16, like, how did i do that?
                           sep=";", converters={"Kyūjitai": jouyoueval}, encoding="utf-16")
    print(jouyoudb)

    jouyoubetter = pd.DataFrame(
        [], columns=["Unicode", "Char", "Kyūjitai", "Grade"])

    for index, row in jouyoudb.iterrows():
        char = row.iloc[0]
        temp = row.iloc[1]
        if temp is np.nan:
            kyuujitailist = np.nan
        else:
            kyuujitailist = list(
                map(lambda x: "U+"+hex(ord(x))[2:].upper(), temp))
        grade = row.iloc[2]
        jouyoubetter = pd.concat([jouyoubetter, pd.DataFrame(
            [["U+"+hex(ord(char))[2:].upper(), char, kyuujitailist, grade]], columns=jouyoubetter.columns)], ignore_index=True)

    jouyoubetter = jouyoubetter.set_index("Unicode")
    jouyoubetter = jouyoubetter.sort_values(
        by="Unicode", key=lambda col: pd.Series([int(x[2:], 16) for x in col]))
    print(jouyoubetter)

    jouyououtput = jouyoubetter.copy()
    jouyououtput["Kyūjitai"] = list(map(
        lambda x: "NaN" if x is np.nan else "[" + ",".join(x) + "]", jouyououtput["Kyūjitai"].tolist()))
    jouyououtput.to_csv(generated + "./jouyou.txt", sep=";")
