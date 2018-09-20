__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from ParsePLA import *

def check(a,b,c,d):
    print (a,b,c,d)
    I_a = a[0]
    I_b = b[0]
    O_a = a[1]
    O_b = b[1]
    for i in range(0,c):
        print (I_a)

    #print (I_a, I_b, O_a, O_b)

d = PARSE_PLA("PLA1")
TT_value = d.get('TT') 
for i in TT_value:
    for j in TT_value:
        check (i,j,d.get('N_IP'),d.get('N_OP'))