import os
from Data import ExtractJouyou
from Decomposition.OLD import ExtractDecomp
from Decomposition.OLD import ExtractDecompFromWiktionary
from Decomposition import ExtractDecompCustoms
from Radicals import ExtractRadicals
from Variants import ExtractVariants
from Variants import ExtractCommonality
from Variants import ExtractHSK

############################# DATA#############################
cwd = os.getcwd()
os.chdir(cwd + "/Data/")
ExtractJouyou.__main__()
###############################################################

######################## DECOMPOSITION#########################
# os.chdir(cwd + "/Decomposition/OLD")
# ExtractDecomp.__main__()
# DO NOT RUN THE WEBSCRAPER EVERY TIME!!!!!
# ExtractDecompFromWiktionary.__main__()
os.chdir(cwd + "/Decomposition/")
ExtractDecompCustoms.__main__()
###############################################################

########################### RADICALS###########################
os.chdir(cwd + "/Radicals/")
ExtractRadicals.__main__()
###############################################################

########################### VARIANTS###########################
os.chdir(cwd + "/Variants/")
ExtractVariants.__main__()
ExtractCommonality.__main__()
ExtractHSK.__main__()
###############################################################
