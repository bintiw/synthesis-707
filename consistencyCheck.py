__author__ = "Carlos Lemus & Brandon Wade"
__version__ = "1.0.1"
__maintainer__ =  "Carlos Lemus & Brandon Wade"
__email__ = "carlosslemus@yahoo.com, bwade.dev@gmail.com"

import sys

"""
checkConsistency will compare the inputs to the outputs to check if the truth table is consistent
P the partition of inputs using getPartitionGroup()
Pf the partiton of outputs using getPartitionGroup()
"""

def checkConsistency(P,Pf):
    interFound = 0; 
    for i in P:
      for k in Pf:
          if(i.issubset(k)):
            interFound += 1
              
      if(interFound == 0):
        sys.exit("Truth Table is not consistent\n")
        exit
      else:
        interFound = 0

    print("Truth Table is consistent\n")


#TODO: Needs revising
def checkConsistency2(TT):
    func = dict()
    for i in range(TT['N_P']+1):
        exp = expand(TT['TT_ip'][i])
        for ii in range(len(exp)):
            #print("***********************************************************iteration ",i)
            if 'x='+str(exp[ii]) not in func:
                #print("pre",func)
                #print("inp",exp[ii])
                #print("out",TT['TT_op'][i])
                func['x='+str(exp[ii])] = TT['TT_op'][i]
                #print("pos",func)
            else:
                #print("compare ",func['x='+str(exp[ii])]," and ",TT['TT_op'][i])
                c = compare(func['x='+str(exp[ii])],TT['TT_op'][i])
                if c == 0:
                    return 0
                elif c > 1:
                    #print("pre",func)
                    #print("inp",exp[ii])
                    #print("out",TT['TT_op'][i])
                    l = TT['TT_op'][i] + copy.deepcopy(func['x='+str(exp[ii])])
                    func.update({'x='+str(exp[ii]): l})
                    #print("pos",func)
    return 1

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

def compare(l, r):
    out = 1
    m = len(r)
    for i in range(len(l)):
        if l[i] != r[i%m] and l[i] != 2 and r[i%m] != 2:
            return 0
        if l[i] != r[i%m] and r[i%m] != 2:
            out += 1
    return out
            
        
        
