__author__ = "Carlos Lemus & Brandon Wade & Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Carlos Lemus & Brandon Wade & Binayak Tiwari"
__email__ = "carlosslemus@yahoo.com, bwade.dev@gmail.com, binayaktiwari@gmail.com"

from utils import *
from encoding import *
from consistencyCheck import *
from compatabilityClasses import *
from itertools import combinations
import math
import operator
import copy
import itertools
   

def main():
    iteration = 0
    filename = input("Please enter the name of the file:")
    B_size = int(input("Please enter an LB size:"))
    i,o = work(filename, iteration, B_size)
    while (not(i==o+1)):
        iteration += 1
        i,o = work("temp", iteration, B_size)

    
    PLA = PARSE_PLA("temp")
    getConsistencyCheck(PLA)
    print("Please check temp file for new table")

def work(file_PLA, iteration, B_size):
    #B_size = 3
    bdex = []

    print("\n---------------------------------------------------------------------------")
    print("\nIteration ",iteration)
    
    PLA = PARSE_PLA(file_PLA)
    partitions = getPartition(PLA)
    
    list_input = PLA.get('IP_LABEL')
    P = getPartitionGroup(list_input,partitions)
    list_output = PLA.get('OP_LABEL')
    Pf = getPartitionGroup(list_output,partitions)

    print("\nCurrent Table")
    print("Cubes: ",len(PLA.get("TT_ip")))
    for line in range(len(PLA.get("TT_ip"))):
        s = ""
        for val in range(len(PLA.get("TT_ip")[line])):
            s += str(PLA.get("TT_ip")[line][val])
        s += "   "
        for val in range(len(PLA.get("TT_op")[line])):
            s += str(PLA.get("TT_op")[line][val])
        print(s)
    
    getConsistencyCheck(PLA)

    AB = getAB(list_input, partitions, B_size)
    #print ("\nAB Choosen:", AB)

    for i in AB['B']:
        bdex.append(PLA.get('IP_LABEL').index(i))

    PA = getPartitionGroup(AB['A'], partitions)
    PB = getPartitionGroup(AB['B'], partitions)

    COM = getCompatabilityClasses(PA,PB,Pf)
    #print ("\nCompatible Classes:",COM)
  
    MCC = getMCC(COM , B_size)
    #print ("\nMaximum Compatible Classes:")
    #for i in MCC:
    #   print (i)

    gray_l = math.ceil(math.log(len(MCC),2)) #gray length
    gray_c = []
    for x in map(''.join, itertools.product('01', repeat=gray_l)):
        gray_c.append(x)
    #gray_c = gray_code(gray_l)
    #print("Ordered Codes:", gray_c)

    if gray_l >= B_size:
        decomp = 0
    else:
        decomp = 1
        
    while(not decomp and B_size < len(list_input)):
        print("\nNo meaningful decomposition, selecting new A and B")
        for comb in combinations(list_input, B_size):
            AB['A'] = []
            AB['B'] = []
            
            for inp in list_input:
                if inp in comb:
                    AB['B'].append(inp)
                else:
                    AB['A'].append(inp)
            bdex = []

            print ("\nNew AB Choosen:", AB)
            
            for i in AB['B']:
                bdex.append(PLA.get('IP_LABEL').index(i))
                
            PA = getPartitionGroup(AB['A'], partitions)
            PB = getPartitionGroup(AB['B'], partitions)


            COM = getCompatabilityClasses(PA,PB,Pf)
            #print ("\nCompatible Classes:",COM)
   
            MCC = getMCC(COM , B_size)
            #print ("\nMaximum Compatible Classes:")
            #for i in MCC:
            #   print (i)

            gray_l = math.ceil(math.log(len(MCC),2)) #gray length
            gray_c = gray_code(gray_l)

            if gray_l < B_size:
                decomp = 1
                break

        if not decomp:
            print("\nNo meaningful decomposition found for B Size = ",B_size,", searching for B Size = ",B_size+1)
            B_size += 1
        else:
            break
                
    if not decomp:
        print("No decomposition found. Quitting program.")
        quit()

    print ("\nAB Choosen:", AB)
    print ("\nCompatible Classes:",COM)
    print ("\nMaximum Compatible Classes:")
    for i in MCC:
       print (i)
    print("\n")
    
    occurs = getOccurences(MCC, PB, PLA["N_P"])
    print ("\nOccurances:")
    print(occurs)

 
    MCC_enc, z, g_code, gray_c= encodeOccurs(occurs, MCC, gray_l, gray_c)
    #print ("\nEncoded MCCs after encoding:", MCC_enc)
    
    #print("\n Z set after encoding:", z) 

    #print("\n g code after encoding:", g_code)

    #print("\nLeft over gray codes: ", gray_c)

    
    #print ("\nMaximum Compatible Classes:",MCC)


    g_table =  getGTable(AB['B'], PLA['N_P'], PLA["TT_ip"],  PLA["IP_LABEL"])
    

    prodPB = getProdPB(PB,g_table)
    
    prodCC = {}

    #cc_B = [[2],[6],[0],[4],[9,5,1],[8],[3,7]]
    cc_B = MCC
    for i in cc_B:
        temp = []
        for j in i:
            #print (j)
            temp.append(prodPB[j])
        prodCC[cc_B.index(i)] = temp
        
    #print("\n g_table: ", g_table)

    z  = step1( g_table, z, g_code)

    #print("\nZ tables after step 1:" , z)

        # transform MCCS tuple to list
        #for i in range(len(MCC)):
        #    MCC[i] = list(MCC[i])


    z,g_table,g_code = step2(z,prodCC,g_table,MCC_enc,g_code)

    #print("\nZ tables after step 2:" , z)

    z,g_table,g_code = step3(z,prodCC,g_table,MCC_enc,g_code)
        #print (z,"\n",g_table,"\n",g_code)

    #print("\nZ tables after step 3:" , z)
    

    g_code, g_table = combine_g_entries(g_code, g_table)
    new_g = []
    new_c = []
    for i in range(len(g_code)):
        if (len(g_table[i])!=0):
            new_g.append(g_table[i])
            new_c.append(g_code[i])

    g_table = new_g
    g_code = new_c
##    for i in range(0,len(g_code)):
##        print (i,"\t",g_table[i],"\t",g_code[i],"\n")


    print("G Table")
    print("Cubes: ", len(g_table))
    for line in range(len(g_table)):
        s = ""
        for val in range(len(g_table[line])):
            s += str(g_table[line][val])
        s += "   "
        for val in range(len(g_code[line])):
            s += str(g_code[line][val])
        print(s)

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

    for iii in range(len(PLA.get('TT_ip'))):
        new_inp = []
        bchk = []
        original_inp =  PLA.get('TT_ip')[iii] #read from original TT

        for i in range(len(original_inp)):
            if i not in bdex:
                new_inp.append(original_inp[i])

        for i in bdex:
            bchk.append(original_inp[i])

        if(bchk in g_table): 
            code_index = g_table.index(bchk) #Find the code index from the Coding Table
            #print(code_index)
        new_TT = new_inp+g_code[code_index] #Replace with code and add remaining A set   

        if ((new_TT+PLA.get('TT_op')[iii]) not in new_entry):
            new_entry.append (new_TT+PLA.get('TT_op')[iii])
        
    f.write(str(len(new_entry))+"\n")
    for i in new_entry:
        ip = i[0:len(i)-len(PLA.get('TT_op')[0])]
        op = i[len(i)-len(PLA.get('TT_op')[0]): len(i)]
        a = ['-' if x==2 else x for x in ip]
        b = ['-' if x==2 else x for x in op]
        
        #print (a, b)
        f.write (''.join(str(e) for e in a) +' '+''.join(str(e) for e in b)+"\n")
    f.write(".e")
    f.close()

    return (len(PLA.get('TT_ip')[0])-B_size+len(g_code[0]),len(PLA.get('TT_op')[0]))
if __name__== "__main__":
  main()
