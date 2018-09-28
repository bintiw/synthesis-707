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
    checkConsistency(P,Pf)

    #get sets A and B
    
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
