# Unihan-Extended-Database-Building-Files

The repo is a collection of python files that will build a merged database of han characters in unicode from several sources (found at the bottom of this file)

# Resources

For explanation of unihan.zip, please see [The tr38 report from Unicode](https://www.unicode.org/reports/tr38/). For any files used, please gather them from here, and place them in the `Data/` folder

`Unihan.zip` can be found [here](https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip) and contains the following relevant files:

1. `Unihan_IRGSources.txt` - Used in files `Radicals/ExtractRadicals.py`.
2. `Unihan_Variants.txt` - Used in files `Variants/ExtractVariants.py`.

`EquivalentUnifiedIdeograph.txt` can be found [here](https://www.unicode.org/Public/17.0.0/ucd/EquivalentUnifiedIdeograph.txt)

- Used in files `Radicals/ExtractRadicals.py`

`char_v1.0.txt` can be found in [this repo](https://github.com/catusf/tudien/releases/tag/V2.6)

- Used in file `Decomposition/ExtractDecomp.py`.

`characterdecomposition.csv` can be found from [this library](https://pypi.org/project/cjklib/) HOWEVER how to get this csv is not so obvious, so please see the 'CJKLib Guide' section down below

- Used in files `TODO`.

For the commonly used characters in China in three files (`level-1.txt`, `level-2.txt`, and `level-3.txt`) please go to [this repo](https://github.com/shengdoushi/common-standard-chinese-characters-table)

- Used in files `Variants/ExtractCommonality.py`.

For `JouyouKanjiExcelt.txt`, please copy the link of [this Wikipedia page](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji), and then follow the steps of the 'Jouyou Kanji List Excel Guide' section down below

- Used in files `Data/ExtractJouyou.py` (and indirectly in `Variants/ExtractCommonality.py`)

`charlist.txt` can be found in [this repo](https://github.com/elkmovie/hsk30/blob/main)

- Used in files `TODO`.

## CJKLib Guide

First, from [the library previously mentioned](https://pypi.org/project/cjklib/), please do the following:

1. Install python 2 (2.4+ at least, but I used [version 2.7.18](https://www.python.org/downloads/release/python-2718/))
2. With this installation, do `pip install cjklib`
3. Now, locate your python install (likely at `C:\Python27\`), and locate the follwing folder: `Lib\site-packages\cjklib\data\`, within it is the `characterdecomposition.csv`

### Bonus steps (Unneccessary)

This is mostly because theres an unexplained command tied to this folder, which goes un explained anywhere, and since I figured out how to make it work with no errors, I figured I'd finish the guide off with these bonus steps.

In case the `Lib\site-packages\cjklib\` folder is missing the `cjklib.db` file, they can be rebuilt in the following way:

4. In the `Lib\site-packages\cjklib\data\` folder, place [an old 2012 version of Unihan.zip](https://www.unicode.org/Public/zipped/6.2.0/Unihan.zip) - (Newer versions of Unihan.zip break the script, there might be a version newer than this one that works though, idk)
5. Run the command `buildcjkdb -r build cjklibData` - (It should be added to your path upon pip install, but if not, you can find the `C:\Python27\Scripts\buildcjkdb.exe` file and maybe run it there?)
6. After running the command and waiting, the database has

## Jouyou excel guide

With the link to the [Jouyou Kanji list Wikipedia page](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji) copied, please do the following:

1. Open MS Excel
2. Go to the `Data` section of the toolbelt
3. Press `New Query` -> `From Other Sources` -> `From Web`
4. In the now open window, paste the URL and press Enter
5. In the now open Navigator window, find the desired table (for me it was `HTML`->`Table 3`), click on it, and then click the `Load` button on the bottom right
6. When the desired table appears, please click the small arrow in the `Grade` column and press `Sort A-Z`
7. Now copy columns `New (Shinjitai)`, `Old (Kyūjitai)`, and `Grade` into a seperate Sheet
8. Rename columns such that they are just called `Shinjitai`, `Kyūjitai`, and `Grade`
9. Now with this sheet open, save as a Unicode (\*.txt) file with name `JouyouKanjiExcel.txt`
10. Open file with notepad, hit ctrl+h to open search and replace
11. Replace `	` with `;`
12. Rejoice

## Other links

### Related but not useful

The [RSIndex.txt](https://www.unicode.org/Public/UCD/latest/charts/RSIndex.txt) file is information partaining to the radical+stroke numbers, which is also present within the `Unihan_IRGSources.txt` file found in `Unihan.zip`

### Unihan history

#### Files from 2010

[CJKU_SR.txt](https://www.unicode.org/L2/L2010/10375-02n4153-files/CJKU_SR.txt),
[CJKC_SR.txt](https://www.unicode.org/L2/L2010/10375-02n4153-files/CJKC_SR.txt), and
[IICORE.txt](https://www.unicode.org/L2/L2010/10375-02n4153-files/IICORE.txt)

#### File from 2013

The [13017-cjk.txt](https://www.unicode.org/L2/L2013/13017-cjk.txt) file states that the above three files (`CJKU_SR.txt`, `CJKC_SR.txt`, and `IICORE.txt`) should be combined into 1 and put into `Unihan.zip`, whose data is now present in the `Unihan_IRGSources.txt` file found in `Unihan.zip`!
