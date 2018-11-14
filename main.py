__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from utils import *
from consistencyCheck import *
from compatabilityClasses import *
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

    #get sets A and B    
    AB = getAB(list_input, partitions, B_size)
    AB = {'A': ['x2'], 'B': ['x1','x4','x0','x3']}

    print ("AB Choosen:", AB)
    print ("\n")
    
    PA = getPartitionGroup(AB['A'], partitions)
    PB = getPartitionGroup(AB['B'], partitions)
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


    COM = getCompatabilityClasses(PA,PB,Pf)
    print ("Compatible Classes:",COM)

   
    #Compatible_list is taken from the lecture slide.
    #compatible_list = [(0,1),(0,3),(1,3),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5),(4,6),(4,7),(5,6)]    # Please modify getCompatabilityClasses to have this kind of pairs returned

    
    #MCC = getMCC(compatible_list , B_size)    
    MCC = getMCC(COM , B_size)
    print ("\nMaximum Compatible Classes:",MCC)

    
    z = [2,4,8,15] # -15
    #g_table = {0: [2,2,0,2], 1:[2,2,0,1], 2:[2,1,2,2],3:[2,0,0,1],4:[1,2,0,0],5:[2,1,0,2],6:[2,1,1,0],7:[2,0,1,1],8:[0,0,0,2],9:[2,1,1,1],10:[0,0,1,1],11:[2,0,0,0],12:[2,1,1,0],13:[2,2,1,0],14:[2,0,1,0],15:[1,2,1,2],16:[2,2,1,0]}
    g_table = [[2,2,0,2],[2,2,0,1],[2,1,2,2],[2,0,0,1],[1,2,0,0],[2,1,0,2],[2,1,1,0],[2,0,1,1],[0,0,0,2],[2,1,1,1],[0,0,1,1],[2,0,0,0],[2,1,1,0],[2,2,1,0],[2,0,1,0],[1,2,1,2],[2,2,1,0]]
    #g_code = {0: [0,2,2], 1:[0,0,2], 2:[],3:[0,0,1],4:[],5:[0,0,0],6:[1,1,1],7:[1,0,2],8:[],9:[0,0,1],10:[1,0,0],11:[0,1,2],12:[1,1,1],13:[],14:[0,0,1],15:[],16:[]}
    g_code = [[0,2,2], [0,0,2],[],[0,0,1],[],[0,0,0],[1,1,1],[1,0,2],[],[0,0,1],[1,0,0],[0,1,2],[1,1,1],[],[0,0,1],[],[]]
    cc_B = [[2],[6],[0],[4],[9,5,1],[8],[3,7]]
    cc = [(7,10),(7,15),(0,8,11),(0,4,11),(0,1,2,3,8,9,13,14,15,16),(2,6,12,13,15,16),(0,1,2,4,5)]
    cc_code = [[1,0,0],[1,0,1],[0,1,0],[0,1,1],[0,0,1],[1,1,1],[0,0,0]]
    gray = [[1,1,0]]

    prodPB = getProdPB(PB,g_table)

    prodCC = {}

    for i in cc_B:
        temp = []
        for j in i:
            temp.append(prodPB[j])
        prodCC[cc_B.index(i)] = temp 


   # print ("Product of CCs::",prodCC)   

    z,g_table,g_code = step2(z,prodCC,g_table,cc_code,g_code)

    print (z,"\n",g_table,"\n",g_code)
   
    for i in range(0,len(g_code)):
        print (i,"\t",g_table[i],"\t",g_code[i],"\n")

if __name__== "__main__":
  main()