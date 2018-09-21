__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from parsePLA import *

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


def get