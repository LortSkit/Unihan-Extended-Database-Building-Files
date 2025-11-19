from Variants import ExtractCommonality
from Variants import ExtractVariants
from Radicals import ExtractRadicals
from Decomposition import ExtractDecomp
from Data import ExtractJouyou
import os

cwd = os.getcwd()
os.chdir(cwd + "/Data/")
ExtractJouyou.__main__()

os.chdir(cwd + "/Decomposition/")
ExtractDecomp.__main__()

os.chdir(cwd + "/Radicals/")
ExtractRadicals.__main__()

os.chdir(cwd + "/Variants/")
ExtractVariants.__main__()
ExtractCommonality.__main__()
