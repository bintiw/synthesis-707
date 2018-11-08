__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from utils import *
from encoding import *
from consistencyCheck import *
from compatabilityClasses import *
import math
import operator

def main():
    B_size = 3
    PLA = PARSE_PLA("PLA3")
    partitions = getPartition(PLA)

    #checkConsistency2(PLA)
    
    list_input = PLA.get('IP_LABEL')
    P = getPartitionGroup(list_input,partitions)
    list_output = PLA.get('OP_LABEL')
    Pf = getPartitionGroup(list_output,partitions)

    
    print ("P: ",P)
    print ("Pf: ",Pf)
    print ("\n")

    # Check Consistency
    #checkConsistency(P,Pf)
    getConsistencyCheck(PLA)

    AB = getAB(list_input, partitions, B_size)
    #AB = {'A': ['x3', 'x4'], 'B': ['x0','x1','x3']}

    print ("AB Choosen:", AB)
    print ("\n")
    
    PA = getPartitionGroup(AB['A'], partitions)
    PB = getPartitionGroup(AB['B'], partitions)
    print ("Set A: ",  PA)
    print ("Set B: ",  PB)
    print ("\n")


    COM = getCompatabilityClasses(PA,PB,Pf)
    print ("Compatible Classes:")
    for i in COM:
        print(i)

   
    #Compatible_list is taken from the lecture slide.
    compatible_list = [(0,1),(0,3),(1,3),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5),(4,6),(4,7),(5,6)]    # Please modify getCompatabilityClasses to have this kind of pairs returned

    
    #MCC = getMCC(compatible_list , B_size)    
    MCC = getMCC(COM , B_size)
    print ("\nMaximum Compatible Classes:")
    #print (MCC)
    for i in MCC:
       print (i)


    print ()
    occurs = getOccurences(MCC, PB)
    print ("\nOccurances:")
    print(occurs)

    gray_l = math.ceil(math.log(len(MCC),2)) #gray length
    gray_c = gray_code(gray_l)
        
  

 
    MCC_enc, z = encodeOccurs(occurs, MCC, gray_l, gray_c)
    print ("\nEncoded MCCs:")
    print(MCC_enc)
    print ("\n Z sets:")
    print(z)

    #step1();

if __name__== "__main__":
  main()
