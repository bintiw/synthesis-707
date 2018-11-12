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
        
  

 
    MCC_enc, z, g_table = encodeOccurs(occurs, MCC, gray_l, gray_c)
    print ("\nEncoded MCCs:")
    print(MCC_enc)
    print("\n")
    
    print("Z set:")
    print(z)
    print("\n")

    print("g table set:")
    print(g_table)

    #step1();

    print ("\nMaximum Compatible Classes:",MCC)

    
    z = [2,4,8,13,16] # -15
    g_table = {0: [2,2,0,2], 1:[2,2,0,1], 2:[2,1,2,2],3:[2,0,0,1],4:[1,2,0,0],5:[2,1,0,2],6:[2,1,1,0],7:[2,0,1,1],8:[0,0,0,2],9:[2,1,1,1],10:[0,0,1,1],11:[2,0,0,0],12:[2,1,1,0],13:[2,2,1,0],14:[2,0,1,0],15:[1,2,1,2],16:[2,2,1,0]}
    g_code = {0: [0,2,2], 1:[0,0,2], 2:[],3:[0,0,1],4:[],5:[0,0,0],6:[1,1,1],7:[1,0,2],8:[],9:[0,0,1],10:[1,0,0],11:[0,1,2],12:[1,1,1],13:[],14:[0,0,1],15:[],16:[]}
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


    
def step2(z,prodCC,g_table,cc_code,g_code):
    print("-----------STEP2--------------","\n")
    #print("Z Set:",z)
    #print("Prod CCs:",prodCC)
    #print("G table",g_table)
    g_table1 = copy.deepcopy(g_table)
    g_code1 = copy.deepcopy(g_code)
    z1 = copy.deepcopy(z)
    for i in z:
        subcubes = expand(g_table[i])
        subcode = []
        for j in subcubes:
            for k in range(0,len(prodCC)):
                for l in prodCC[k]:
                    subcubes_prodcc = expand(l)
                    if(j in subcubes_prodcc):
                        subcode.append(cc_code[k])
        list2 = [x for x in subcode if x]
        subcode = list2
        if(len(subcode)==len(subcubes)):
            print (i,z1,subcubes,subcode)
            g_table1[i] = subcubes[0]
            g_code1[i] = subcode[0]

            for m in range(1,len(subcubes)):
                g_table1.update({len(g_table1) : subcubes[m]})
                g_code1.update({len(g_code1) : subcode[m]})
            z1.remove(i)
    print("-----------STEP2---Done-----------","\n")  
    return z1,g_table1,g_code1

        

if __name__== "__main__":
  main()
