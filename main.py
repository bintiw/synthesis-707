__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from utils import *
from consistencyCheck import *
from compatabilityClasses import *

def main():
    B_size = 3
    PLA = PARSE_PLA("PLA1")

    #checkConsistency2(PLA)
    
    list_input = PLA.get('IP_LABEL')
    P = getPartitionGroup(list_input,getPartition(PLA))
    list_output = PLA.get('OP_LABEL')
    Pf = getPartitionGroup(list_output,getPartition(PLA))

    
    print ("P: ",P)
    print ("Pf: ",Pf)
    print ("\n")

    # Check Consistency
    checkConsistency(P,Pf)

    #get sets A and B
    partitions = getPartition(PLA)
    AB = getAB(list_input, partitions, 3)
    print ("AB Choosen:", AB)
    
    PA = getPartitionGroup(AB['A'], partitions)
    PB = getPartitionGroup(AB['B'], partitions)
    print ("Set A: ",  PA)
    print ("Set B: ",  PB)

    COM = getCompatabilityClasses(PA,PB,Pf)

    #print(COM)

if __name__== "__main__":
  main()
