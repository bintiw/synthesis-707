__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from parsePLA import *
import itertools
import sys

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



