# Unihan-Extended-Database-Building-Files

The repo is a collection of python files that will build a merged database of han characters in unicode from several sources (found at the bottom of this file). For certain generated files whose creation script have a long runtime like, e.g. `decomp_scrape.text`, they will be saved in the `Data/Generated/` folder. The others might later be accessible through Github Pages, but this is currently a TODO.

# Unicode Han Characters Overview

There are a lot of relevant Unicode blocks to go through, some of which have gaps. Here is the overview of what is and isn't counted as relevant blocks:

## Counted

```
U+2E80..U+2EFF - CJK Radicals Supplement:-------------------Is missing U+2E9A, and U+2EF4..U+2EFF
U+2F00..U+2FDF - Kangxi Radicals:---------------------------Is missing U+2FD6..U+2FDF
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+3400..U+4DBF - CJK Unified Ideographs Extension A:--------Block is full
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+4E00..U+9FFF - CJK Unified Ideographs:--------------------Block is full
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+F900..U+FAFF - CJK Compatibility Ideographs:--------------Is missing U+FA6E..U+FA6F, and U+FADA..U+FAFF
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+20000..U+2A6DF - CJK Unified Ideographs Extension B:------Block is full
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+2A700..U+2B73F - CJK Unified Ideographs Extension C:------Block is full
U+2B740..U+2B81F - CJK Unified Ideographs Extension D:------Is missing U+2B81E..U+2B81F
U+2B820..U+2CEAF - CJK Unified Ideographs Extension E:------Is missing U+2CEAE..U+2CEAF
U+2CEB0..U+2EBEF - CJK Unified Ideographs Extension F:------Is missing U+2EBE1..U+2EBEF
U+2EBF0..U+2EE5F - CJK Unified Ideographs Extension I:------Is missing U+2EE5E..U+2EE5F
U+2F800..U+2FA1F - CJK Compatibility Ideographs Supplement:-Is missing U+2FA1E..U+2FA1F
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+30000..U+3134F - CJK Unified Ideographs Extension G:------U+3134B..U+3134F
U+31350..U+323AF - CJK Unified Ideographs Extension H:------Block is full
U+323B0..U+3347F - CJK Unified Ideographs Extension J:------U+3347A..U+3347F
```

## Not counted

The possibly relevant blocks that are not counted are displayed here

```
U+2FF0..U+2FFF - Ideographic Description Characters (NOT CHARS): Block is full
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Gap%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
U+31C0..U+31EF - CJK Strokes (NOT CHARS):                        Is missing U+31E6..U+31EE
```

# Resources

This is how to attain all the resources needed for the `RunAll.py` script to run. When attained, they have to be placed in the `Data/Resources/` folder - NOTE: `JouyouKanjiExcelt.txt` needs a little extra work to be made in the right format, so refer to its guide below for more information.

For explanation of unihan.zip, please see [The tr38 report from Unicode](https://www.unicode.org/reports/tr38/). For any files used, please gather them from here, and place them in the `Data/` folder

`Unihan.zip` can be found [here](https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip) and contains the following relevant files:

1. `Unihan_IRGSources.txt` - Used in files `Radicals/ExtractRadicals.py`.
2. `Unihan_Variants.txt` - Used in files `Variants/ExtractVariants.py`.

For `JouyouKanjiExcelt.txt`, please copy the link of [this Wikipedia page](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji), and then follow the steps of the 'Jouyou Kanji List Excel Guide' section down below

- Used in files `Data/ExtractJouyou.py` (and indirectly in `Variants/ExtractCommonality.py`)

`char_v1.0.txt` can be found in [this repo](https://github.com/catusf/tudien/releases/tag/V2.6)

- Used in file `Decomposition/ExtractDecomp.py`.

`EquivalentUnifiedIdeograph.txt` can be found [here](https://www.unicode.org/Public/17.0.0/ucd/EquivalentUnifiedIdeograph.txt)

- Used in files `Radicals/ExtractRadicals.py`

For the commonly used characters in China in three files (`level-1.txt`, `level-2.txt`, and `level-3.txt`) please go to [this repo](https://github.com/shengdoushi/common-standard-chinese-characters-table)

- Used in files `Variants/ExtractCommonality.py`.

`charlist.txt` can be found in [this repo](https://github.com/elkmovie/hsk30/blob/main)

- Used in files `ExtractHSK.py`.

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
11. Replace '&ensp;' with ';'
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
