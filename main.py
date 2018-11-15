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
import copy       

def main():
    B_size = 4
    PLA = PARSE_PLA("PLA4")
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
    #AB = {'A': ['x2'], 'B': ['x1','x4','x0','x3']}

    print ("AB Choosen:", AB)
    print ("\n")

    PA = getPartitionGroup(AB['A'], partitions)
    PB = getPartitionGroup(AB['B'], partitions)

    #print(partitions)
    tempPB = copy.deepcopy(PB)
    PB = remove_(PB)

    s = []

    """
    Removing duplicate or subsets in PB
    """
    for i in range(0,len(PB)):
        flag = 0
        for j in range(0,len(PB)):
            if (i!=j):
                if(PB[i].issubset(PB[j])):
                    flag = 1
        if(flag == 0):
            s.append(PB[i])

    PB = s
    
                
    print ("Set A: ",  PA)
    print ("Set B: ",  PB)
    print ("\n")


    COM = getCompatabilityClasses(PA,tempPB,Pf)
    print ("Compatible Classes:",COM)

   
    #Compatible_list is taken from the lecture slide.
    #compatible_list = [(0,1),(0,3),(1,3),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5),(4,6),(4,7),(5,6)]    # Please modify getCompatabilityClasses to have this kind of pairs returned

    
    #MCC = getMCC(compatible_list , B_size)    
    MCC = getMCC(COM , B_size)
    print ("\nMaximum Compatible Classes:")
    #print (MCC)
    for i in MCC:
       print (i)


    occurs = getOccurences(MCC, tempPB, PLA["N_P"])
    print ("\nOccurances:")
    print(occurs)

    gray_l = math.ceil(math.log(len(MCC),2)) #gray length
    gray_c = gray_code(gray_l)
        
  

 
    MCC_enc, z, g_code = encodeOccurs(occurs, MCC, gray_l, gray_c)
    print ("\nEncoded MCCs after encoding                       :")
    print(MCC_enc)
    
    print("\n Z set after encoding:", z) 

    print("\n g code after encoding:")
    print(g_code)

    
    print ("\nMaximum Compatible Classes:",MCC)


    g_table =  getGTable(AB['B'], PLA['N_P'], PLA["TT_ip"],  PLA["IP_LABEL"])
    

    prodPB = getProdPB(PB,g_table)

    prodCC = {}

    cc_B = [[2],[6],[0],[4],[9,5,1],[8],[3,7]]
    
    for i in cc_B:
        temp = []
        for j in i:
            temp.append(prodPB[j])
        prodCC[cc_B.index(i)] = temp
        
    print("\n g_table: ", g_table)
    
    z = step1( g_table, z, g_code)

    print("\nZ tables step 1 removed:" , z)

    # transform MCCS tuple to list
    #for i in range(len(MCC)):
    #    MCC[i] = list(MCC[i])





    z,g_table,g_code = step2(z,prodCC,g_table,MCC_enc,g_code)

    print("\nZ tables step 2 removed:" , z)
    
    for i in range(0,len(g_code)):
        print (i,"\t",g_table[i],"\t",g_code[i],"\n")

if __name__== "__main__":
  main()
