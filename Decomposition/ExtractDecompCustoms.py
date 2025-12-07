import numpy as np
import pandas as pd
import os
import re

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"
handwritten = datafolder + "Handwritten/"


def myeval(x):
    return x


def __main__():
    with open(resources + "IDS.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f]
        f.close()

    output = ["Nr;Decomposition"]

    for i, line in enumerate(lines):
        # print(i)
        if not line.startswith("#	{"):
            continue

        temp = line.split("#	{")
        nr = temp[1].split("}	")[0]

        temp = temp[1].split(" of ")
        if len(temp) < 2 and "without" not in temp[0] and "hooked" not in temp[0]:
            output.append(nr.replace("}", "") + ";NaN")
            continue

        if len(temp) > 2:
            temp = temp[2]
        elif "without" not in temp[0] and "hooked" not in temp[0]:
            temp = temp[1]
        else:
            # print("WTF" + str(temp))
            temp = temp[0]

        temp = temp.split("	")
        # print("Nr: " + nr + ", Temp: " + str(temp))
        if len(temp) < 2 and "without" not in temp[0] and "hooked" not in temp[0]:
            output.append(nr + ";NaN")
            continue
        elif "without" not in temp[1] and "hooked" not in temp[1]:
            decomp = temp[1]
        else:
            decomp = temp[2]

        if decomp == "？":
            output.append(nr+";NaN")
        else:
            output.append(nr+";"+decomp)

        if nr == "122":
            break

    outputfile = "\n".join(output)

    with open(generated + "IDS_extracted_customs.txt", "w", encoding="utf-8")as o:
        o.write(outputfile)
        o.close()

    db = pd.read_csv(generated + "IDS_extracted_customs.txt",
                     sep=";", encoding="utf-8", converters={"Nr": myeval, "Decomposition": myeval})
    replacements = pd.read_csv(
        handwritten + "IDS_customs_replacements.text", sep=";", encoding="utf-8", header=None, converters={0: myeval, 1: myeval})
    replacements.columns = db.columns
    replacements = replacements.set_index("Nr")
    db = db.set_index("Nr")
    for nr, row in replacements.iterrows():
        # print(nr + ": Replacing " +
        #       db.loc[nr, "Decomposition"] + " with " + row["Decomposition"])
        db.loc[nr, "Decomposition"] = row["Decomposition"]

    print(db)
    db.to_csv(generated + "IDS_customs_final.txt", sep=";", encoding="utf-8")


if __name__ == "__main__":
    __main__()
