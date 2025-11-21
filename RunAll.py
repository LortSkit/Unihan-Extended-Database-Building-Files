from Variants import ExtractCommonality
from Variants import ExtractVariants
from Radicals import ExtractRadicals
from Decomposition import ExtractDecomp
from Data import ExtractJouyou
from Variants import ExtractHSK
import os

############################# DATA#############################
cwd = os.getcwd()
os.chdir(cwd + "/Data/")
ExtractJouyou.__main__()
###############################################################

######################## DECOMPOSITION#########################
os.chdir(cwd + "/Decomposition/")
ExtractDecomp.__main__()
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
# DO NOT RUN THE WEBSCRAPER EVERY TIME!!!!!
###############################################################
