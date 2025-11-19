# File made for explorative purposes

import numpy as np
import pandas as pd

datafolder = "../Data/"


def myeval(x):
    if x == "NaN":
        return np.nan

    tempx = x[1:-1]  # removes [ and ]
    return tempx.split(",")


def contains(series1, series2):
    if len(series1) != len(series2):
        raise Exception("Bro...")

    output = []

    for i, val in enumerate(series1):
        output.append(val in series2[i])

    return output


def flip(listt):
    return list(map(lambda x: not x, listt))


def notin(series, listt):

    output = []

    for i, row in series.iterrows():
        output.append(not (i in listt))

    return output


def inn(series, listt):

    output = []

    for i, row in series.iterrows():
        output.append(i in listt)

    return output


def combineforcount(l1, l2):
    output = l1.copy()

    for elem in l2:
        if elem not in output:
            output.append(elem)
    return output


def overlap(l1, l2):
    output = []
    for elem in l1:
        if (elem in l2) and (elem not in output):
            output.append(elem)

    for elem in l2:
        if (elem in l1) and (elem not in output):
            output.append(elem)

    return output


db = pd.read_csv(datafolder + "variants.txt", sep=";", converters={'CSimplified': myeval, 'CTraditional': myeval,
                 'CSemanticVariant': myeval, 'CContextDependentVariant': myeval, 'CShapeVariant': myeval, 'AMistakenVariant': myeval})
db = db.set_index("Unicode")
print(db)

temp = db.loc[db["CSimplified"].notnull()]
simptradall = temp.loc[temp["CTraditional"].notnull()]
print(simptradall)

# apparently only one character (U+82E7 苧)
hard = simptradall[flip(
    contains(simptradall.index, simptradall["CSimplified"]))]
print(hard)

simptrad = simptradall[contains(simptradall.index, simptradall["CSimplified"])]
print(simptrad)

tradonly = temp.loc[temp["CTraditional"].isnull()]
print(tradonly)

temp2 = db.loc[db["CTraditional"].notnull()]
simponly = temp2.loc[temp2["CSimplified"].isnull()]
print(simponly)

temp3 = db.loc[db["CTraditional"].isnull()]
justvariants = temp3.loc[temp3["CSimplified"].isnull()]
print(justvariants)

print(len(hard)+len(simptrad)+len(tradonly) +
      len(simponly)+len(justvariants), "=", len(db))

trads = []
coveredsimps = []
for index, row in tradonly.iterrows():
    shorthand = row["CSimplified"]
    for elem in shorthand:
        if (elem not in simponly.index) and (index not in trads):
            trads.append(index)
        elif (elem in simponly.index) and (elem not in coveredsimps):
            coveredsimps.append(elem)

simps = []
coveredtrads = []
for index, row in simponly.iterrows():
    shorthand = row["CTraditional"]
    for elem in shorthand:
        if (elem not in tradonly.index) and (index not in simps):
            simps.append(index)
        elif (elem in tradonly.index) and (elem not in coveredtrads):
            coveredtrads.append(elem)

# print(len(simptrad)+len(hard), "?=?", len(tradonly)-len(simponly))
# print(count, "?=?", len(tradonly)-len(simponly))
# print(count2, "?=?", len(tradonly)-len(simponly))
# print(count-count2, "?=?", len(tradonly)-len(simponly))
# print(len(coveredtrads)-len(coveredsimps), "?=?", len(tradonly)-len(simponly))
print(len(coveredsimps) + len(simps), "=", len(simponly))
print(len(combineforcount(coveredsimps, simps)), "=", len(simponly))
print(len(coveredtrads) + len(trads), "=/=", len(tradonly))
print(len(combineforcount(coveredtrads, trads)), "=", len(tradonly))
overlapping = overlap(coveredtrads, trads)
print(len(coveredtrads) + len(trads) - len(overlapping), "=", len(tradonly))
print(len(simponly) + len(simptradall) +
      len(overlapping), "?=?", len(tradonly))
overlaps = tradonly[inn(tradonly, overlapping)]
print(overlaps)  # len 27

interestingsimps1 = []
interestingsimps2 = []
for index, row in overlaps.iterrows():
    shorthand = row["CSimplified"]
    beforelen = len(interestingsimps1)
    for elem in shorthand:
        if (elem not in simponly.index) and (elem not in interestingsimps1):
            interestingsimps1.append(elem)
        elif (elem in simponly.index) and (elem not in interestingsimps2):
            interestingsimps2.append(elem)

interesting1 = simptradall[inn(simptradall, interestingsimps1)]
print(interesting1)  # len 27

interesting2 = simponly[inn(simponly, interestingsimps2)]
print(interesting2)  # len 27

i = 0
for index, row in overlaps.iterrows():
    print(index + ": " + row["Char"] + " -> " +
          chr(int(interestingsimps1[i][2:], 16)) + " and " + chr(int(interestingsimps2[i][2:], 16)))
    i += 1

print(db.loc[db.index == "U+4E9E"])
print(db.loc[db.index == "U+20124"])  # Missing kyuujitai simplification
print(db.loc[db.index == "U+4E9A"])
