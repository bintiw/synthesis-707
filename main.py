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
    i,o = work("RD84")
    while (not(i==o+1)):
        i,o = work("temp")


def work(file_PLA):
    B_size = 4
    PLA = PARSE_PLA(file_PLA)
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
    print ("Set B: ",  tempPB)
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
    #print ("\nOccurances:")
    #print(occurs)

    gray_l = math.ceil(math.log(len(MCC),2)) #gray length
    gray_c = gray_code(gray_l)
        
  

 
    MCC_enc, z, g_code, gray_c= encodeOccurs(occurs, MCC, gray_l, gray_c)
    print ("\nEncoded MCCs after encoding:", MCC_enc)
    
    print("\n Z set after encoding:", z) 

    #print("\n g code after encoding:", g_code)

    print("\nLeft over gray codes: ", gray_c)

    
    print ("\nMaximum Compatible Classes:",MCC)


    g_table =  getGTable(AB['B'], PLA['N_P'], PLA["TT_ip"],  PLA["IP_LABEL"])
    

    prodPB = getProdPB(PB,g_table)

    prodCC = {}

    #cc_B = [[2],[6],[0],[4],[9,5,1],[8],[3,7]]
    cc_B = MCC
    for i in cc_B:
        temp = []
        for j in i:
            print (j)
            temp.append(prodPB[j])
        prodCC[cc_B.index(i)] = temp
        
    #print("\n g_table: ", g_table)

    z  = step1( g_table, z, g_code)

    print("\nZ tables after step 1:" , z)

        # transform MCCS tuple to list
        #for i in range(len(MCC)):
        #    MCC[i] = list(MCC[i])



    z,g_table,g_code = step2(z,prodCC,g_table,MCC_enc,g_code)

    print("\nZ tables after step 2:" , z)

    z,g_table,g_code = step3(z,prodCC,g_table,MCC_enc,g_code)
        #print (z,"\n",g_table,"\n",g_code)

    print("\nZ tables after step 3:" , z)
    

    g_code, g_table = combine_g_entries(g_code, g_table)
    for i in range(0,len(g_code)):
        print (i,"\t",g_table[i],"\t",g_code[i],"\n")


    for i in range (len(g_code)):
        if(g_code[i] == []):
            if (len(gray_c)==0):
                print ("We ran out of code...")
                exit()
            else:
                g_code[i] = gray_c.pop()
            


    #for checking in range(0,len(g_table):
     #   for comparing in range(1, len(g_tabLe):
      #      for bitsChecking in range(0, len(checking)):
       #         if(g_table[checking][bitsChecking] == g_table[comparing][bitsComparing]

    new_entry=[]
    f =open("temp","w+")
    
    f.write(".i "+ str(len(PLA.get('TT_ip')[0])-B_size+len(g_code[0]))+"\n")
    f.write(".o "+ str(len(PLA.get('TT_op')[0]))+"\n")
    f.write(".ilb")
    for iii in range(len(PLA.get('TT_ip')[0])-B_size+len(g_code[0])):
        f.write(" ")
        f.write("x"+str(iii))
    f.write("\n"+".ob")
   
    for iii in range(len(PLA.get('TT_op')[0])):
        f.write(" ")
        f.write("y"+str(iii))
    f.write("\n"+".p ")

    for j in range(len(PLA.get('TT_ip'))):
        original_TT =  PLA.get('TT_ip')[j] #read from original TT
        #print(original_TT) 
        B_set_TT = original_TT[0:B_size] #strip B set from original TT 
        #print(B_set_TT) 
        if(original_TT[0:B_size] in g_table): 
            code_index = g_table.index(original_TT[0:B_size]) #Find the code index from the Coding Table
            #print(code_index)
        new_TT = original_TT[B_size:len(original_TT)]+g_code[code_index] #Replace with code and add remaining A set 
        
        
        #new_entry_ip = ''.join(str(e) for e in new_TT) # Create a new PLA entry
        #new_entry_op = ''.join(str(e) for e in PLA.get('TT_op')[j])
        if ((new_TT+PLA.get('TT_op')[j]) not in new_entry):
            new_entry.append (new_TT+PLA.get('TT_op')[j])
    f.write(str(len(new_entry))+"\n")
    for i in new_entry:
        ip = i[0:len(i)-len(PLA.get('TT_op')[0])]
        op = i[len(i)-len(PLA.get('TT_op')[0]): len(i)]
        #print (ip, op)
        f.write (''.join(str(e) for e in ip) +' '+''.join(str(e) for e in op)+"\n")
    f.write(".e")
    f.close()

    return (len(PLA.get('TT_ip')[0])-B_size+len(g_code[0]),len(PLA.get('TT_op')[0]))
if __name__== "__main__":
  main()
