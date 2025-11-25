import numpy as np
import pandas as pd

datafolder = "../Data/"
resources = datafolder + "Resources/"
generated = datafolder + "Generated/"


def __main__():
    decomp = pd.read_csv(
        generated + "decomp_scrape_clean.text", sep=";", encoding="utf-8")
    decomp = decomp.set_index("Unicode")
    hasdecomp = decomp[~decomp["Decomposition"].isna()]
    print(hasdecomp)
    # testdecomp = hasdecomp.loc["U+2E81"]["Decomposition"]
    # testdecomp2 = hasdecomp.loc["U+341A"]["Decomposition"]
    decomp["WEqual"] = ["NaN"] * len(decomp)
    for i, (unicode, row) in enumerate(decomp.iterrows()):
        if i % 1000 == 0:
            print("Progress: " + str(i//1000) + "/103")
        if unicode not in hasdecomp.index:
            continue
        decompval = row["Decomposition"]
        if decompval is np.nan:
            continue
        searchdf = decomp[decomp["Decomposition"] == decompval]
        if len(searchdf) >= 2:
            listofunicodes = []
            for unimatch, _ in searchdf.iterrows():
                if unimatch == unicode:
                    continue
                listofunicodes.append(unimatch)
            decomp.loc[unicode, "WEqual"] = listofunicodes.__repr__().replace(
                "'", "")

    multiples = decomp[decomp["WEqual"] != "NaN"]
    print(multiples)
    decomp.to_csv(generated + "decomp_test.txt", sep=";", encoding="utf-8")
    multiples.to_csv(generated + "multiples.txt",
                     sep=";", encoding="utf-8")

    # TODO: Remove '\u's and see if anything from UniqueMultiples.py is worth adding


if __name__ == "__main__":
    __main__()
