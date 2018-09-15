__author__ = "Binayak Tiwari"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

import re

_PLA_FILENAME = "PLA1"

PLA_COMMENT = re.compile(r"^#(.*$)")
PLA_TYPE = re.compile(r'^.type\s+(f|r|fr|fd|dr|fdr)$') 
PLA_INP= re.compile(r'^.i\s+((\d)+)$')
PLA_OUT= re.compile(r'^.o\s+((\d)+)$')
PLA_ILB = re.compile(r'^.ilb\s+((\w+\s?)+)$')
PLA_OB= re.compile(r'^.ob\s+((\w+\s?)+)$')
PLA_P= re.compile(r'^.p\s+((\d)+)$')
PLA_TT= re.compile(r"^([01-]+)\s+([01-]+)$")

f = open(_PLA_FILENAME,"r")
s = f.readlines()

for lines in s:
    #print (lines)
    catch_TYPE = PLA_TYPE.match(lines)
    if(catch_TYPE):
        try:
            print("TYPE:",catch_TYPE.group(1))
        except Exception:
            print("Error in .type description")

    catch_INP = PLA_INP.match(lines)
    if(catch_INP):
        try:
            print("Input:",catch_INP.group(1))
        except Exception:
            print("Error in .i description")

    catch_OUT = PLA_OUT.match(lines)
    if(catch_OUT):
        try:
            print("Output",catch_OUT.group(1))
        except Exception:
            print("Error in .o description")

    catch_COMMENT = PLA_COMMENT.match(lines)
    if(catch_COMMENT):
        try:
            print("Comment:",catch_COMMENT.group(1))
        except Exception:
            print("Error in writing comment")

    catch_ILB = PLA_ILB.match(lines)
    if(catch_ILB):
        try:
            print("Ip Signals:",catch_ILB.group(1))
        except Exception:
            print("Error in .ilb description")

    catch_OB = PLA_OB.match(lines)
    if(catch_OB):
        try:
            print("Op Signals:",catch_OB.group(1))
        except Exception:
            print("Error in .ob description")
    
    catch_P = PLA_P.match(lines)
    if(catch_P):
        try:
            print("Row in TT:",catch_P.group(1))
        except Exception:
            print("Error in .p description")

    catch_TT = PLA_TT.match(lines)
    if(catch_TT):
        try:
            print(catch_TT.group(1),catch_TT.group(2) )
        except Exception:
            print("Error in Truth Table description")



#s = ".ilb in1 input carry enable"

#print((re.compile(r"^.ilb\s+(\w+(?:\s+\w+)*)$")).match(s))
#print((re.compile(r'^.ilb\s+((\w+\s?)+)$')).match(s).group(1))

