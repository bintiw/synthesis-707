__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from parsePLA import *
import itertools
import numpy as np

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
    
