__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from parsePLA import *
import itertools
import sys
import copy




import numpy as np

def getGTable(B, N_P, TT_ip):
    g_table = [[] for _ in range(N_P)]
    g_sorted = sorted(B)
    for inp_indx in range(N_P):
        for x in g_sorted:
            g_table[inp_indx].append(TT_ip[inp_indx][int(x[-1])])

    return g_table

def gray_code(n):
    def gray_code_recurse (g,n):
        k=len(g)
        if n<=0:
            return

        else:
            for i in range (k-1,-1,-1):
                char='1'+g[i]
                g.append(char)
            for i in range (k-1,-1,-1):
                g[i]='0'+g[i]

            gray_code_recurse (g,n-1)

    g=['0','1']
    gray_code_recurse(g,n-1)
    return g


"""
Get product of all elements of MCC for step2
"""
def getProdPB(PB,g_table):
    #print ("----GET PROD----")
    #print ("PB:",PB)
    #print ("g_table:",g_table)
    prod = {}
    for i in range(0,len(PB)):
        temp = []
        prod_temp = []
        for j in list(PB[i]):
            temp.append(g_table[j])
        #print ("HERE::::::::",temp)
        a = np. array(temp)
        #print (a)
        for k in range(0,len(a[0])):
                b = a[:,k]
                #print (b)
                b = np.unique(b)
                #print (b)
                if(1 in b and 2 in b and 0 in b):
                    prod_temp.append(3)
                elif (1 not in b and 2 not in b):
                    prod_temp.append(0)
                elif (0 not in b and 2 not in b):
                    prod_temp.append (1)
                elif (1 not in b and 0 not in b):
                    prod_temp.append (2)
                elif (0 in b and 2 in b):
                    prod_temp.append (0)
                elif (1 in b and 2 in b):
                    prod_temp.append (1)
                elif (1 in b and 0 in b):
                    prod_temp.append (3)
                else:
                    prod_temp.append (4)
        prod.update({i:prod_temp})    
    return (prod)
"""
getPartition is the function that takes in a parsed PLA description as an input 
and returns dictionary of input and output literal partition
"""
def getPartition(d):
    P = dict()
    partition = []
    for i in range(0,d.get('N_IP')):
        p_pla = list(item[i] for item in d.get('TT_ip'))
        p_0 = set([ii for ii, x in enumerate(p_pla) if ((x == 0) or (x==2))])
        partition.append(p_0)
        p_0 = set([ii for ii, x in enumerate(p_pla) if ((x == 1) or (x==2))])
        partition.append(p_0)
        P["P("+str(d.get("IP_LABEL")[i])+")"] = list(partition)
        partition.clear()


    for i in range(0,d.get('N_OP')):
        p_pla = list(item[i] for item in d.get('TT_op'))
        p_0 = set([ii for ii, x in enumerate(p_pla) if ((x == 0) or (x==2))])
        partition.append(p_0)
        p_0 = set([ii for ii, x in enumerate(p_pla) if ((x == 1) or (x==2))])
        partition.append(p_0)
        P['P('+d.get('OP_LABEL')[i]+')'] = list(partition)
        partition.clear()
    return (P)


"""
getPartitionGroup will generate a partition for P(x0,x1,x2...xn)
input is the list of literals whose partition is required and individal partition 
dictionary obtained from getPartition() function
"""

def getPartitionGroup(list_input, d1):
    for j in range(len(list_input)):
            globals()[list_input[j].format(j)] = d1['P('+list_input[j]+')']
            

    #for j in list_input:
    #print (globals()['x2'])

    set_grp = list()
    aa = set()
    for x in itertools.product(range(2),repeat=len(list_input)):
        aa = globals()[list_input[0]][x[0]]
        for i in range(1,len(x)):
           globals()['variable{}'.format(i)] = globals()[list_input[i]][x[i]]
           aa = aa & (globals()['variable{}'.format(i)])
        set_grp.append(aa)
    return (set_grp)

"""
getIntersection returns a list of intersections between to lists of sets
P0 list of sets
P1 list of sets
"""
def getIntersections(P0, P1):
    Po = []
    for i in P0:
        for ii in P1:
            Po.append(i.intersection(ii))

    return Po

"""
This is a function to check the consistency of the TT

Needs to be TESTED , not COMPLETELY TESTED
"""

def getConsistencyCheck(d1):
    TT_={}
    strIP = ""
    
    for i in range(0,len(d1['TT_ip'])):
        str1  = ''.join(map(str, d1['TT_ip'][i]))
        strIP = strIP+str1+";"
        
        str2  = ''.join(map(str, d1['TT_op'][i]))
        #strOP = strOP+str1+";"

        #print (str1,str2)
        if(str1 in TT_.keys()):
            if(str2 != TT_[str1]):
                print("Consistency Fail")
                sys.exit("Consistency Fail")
        TT_[str1] = str2


    #print (TT_)
    for i in range(0,len(d1['TT_ip'])):
        str1  = ''.join(map(str, d1['TT_ip'][i]))

        str2 = TT_[str1]
        
        str2 = re.sub('0' ,'(0|2)', str2)
        str2 = re.sub('1' ,'(1|2)', str2)
        str2 = re.sub('(?<!\|)2' ,'[012]', str2)
        
        str1 = re.sub('0' ,'(0|2)', str1)
        str1 = re.sub('1' ,'(1|2)', str1)
        str1 = re.sub('(?<!\|)2' ,'[012]', str1)

        #print ("IP Matching:",str1,"OP Matching:",str2)
        #print("Checking ...",str1,strIP)
        patternIP = re.compile(str1)
        matchesIP = patternIP.finditer(strIP)
        
        strOP = ""
        length1 = 0
        length2 = 0
        for match in matchesIP:
            length1 = length1+1
            strOP = strOP+''.join(map(str, TT_[match.group()]))+";"
           # print (match.group(),TT_[match.group()])

        patternOP = re.compile(str2)
        matchesOP = patternOP.finditer(strOP)
        for match in matchesOP:
            length2 = length2+1

        #print ("length:",length1,length2)
        if(length1!=length2):
            print ("Consistency FAIL")
            sys.exit("Consistency Fail")
    print("----------------Consistency PASS---------------------")    

"""
Function to remove duplicate item in a list
"""
def remove_(duplicate): 
    final_list = [] 
    for num in duplicate:
        if num not in final_list:
            if len(num)!=0:
                    final_list.append(num)
                
    return final_list

"""
function to remove all subsets, only keeps a superset
Helper function for getMCC()
"""

def remove_MCC_redundant(duplicate):
    final = []
    for i in duplicate:
        flag = 0
        for j in duplicate:
            if (i.issubset(j) and i!=j):
                flag =1
        if flag==0:
            final.append(i)
    return final

"""
Returns maximum compatible classes
Needs testing, only after getCompatiblityClasses returns list of tuples of compatible pairs
"""

def getMCC(com,B_size):
    CC = [set()]
    S = set()
    res = set()
    for i in range(0,2**B_size):
        S.clear()
        for j in com:
            if(i==j[1]):
                S.add(j[0])
        #print("S=",S)
        #print("C=",CC)  
        CC_ = CC
        for k in range(0,len(CC_)):
            res = set()
            res = CC_[k].intersection(S)
            #print("Intersection (SnC)=",CC_[k],S,res)
            res.add(i)
            CC.append(res)
            CC = remove_(CC)
            #CC = remove_MCC_redundant(CC)
            #print("Added to (SnC)=",CC)
        #print("-----------")
    ret = []
    for i in remove_MCC_redundant(CC):
        ret.append(tuple(i))
    #print (ret)

    return (ret)

"""
Compatibility check for step2
"""
def compatibilityCheck(a,b):
    for i in range(len(a)):   
        if (not((a[i]==2 and b[i] ==0) or (a[i]==2 and b[i] ==1)or (a[i]==0 and b[i] ==0) or (a[i]==1 and b[i] ==1))):
            return 0
        
    return 1

"""
Function to find subcube of the expression
Carlos and Brandon's Code
"""
def expand(v):
    exp = [[]]
    for i in range(len(v)):
        if v[i]==2:
            exp.extend(copy.deepcopy(exp))
            for ii in range(len(exp)):
                if(ii < len(exp)/2):
                    exp[ii].append(0)
                else:
                    exp[ii].append(1)
        else:
            for ii in range(len(exp)):
                exp[ii].append(copy.deepcopy(v[i]))
    return exp


"""
code to locate a duplicate entry in list
"""

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs
#compatible_list = [(0,1),(0,3),(1,3),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5),(4,6),(4,7),(5,6)]
#getMCC(compatible_list , 3)
