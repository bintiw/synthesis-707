__author__ = "Carlos Lemus & Brandon Wade"
__version__ = "1.0.1"
__maintainer__ =  "Carlos Lemus & Brandon Wade"
__email__ = "carlosslemus@yahoo.com, bwade.dev@gmail.com"

from utils import *

"""
getAB will generate a dictionary of sets A and B that can be decomposed
input is the list of literals whose partition is required and individal partition 
partitions list of partitions from getPartition()
B_size the size of the B that should be broken down, depending on circuitry
"""
def getAB(list_input, partitions, B_size):

    A = []
    B = []
    AA = []
    BB = []
    differences = []

    # Get the difference of 1s and 0s for each input and store in array
    for i in range(len(list_input)):
         globals()[list_input[i].format(i)] = partitions['P('+list_input[i]+')']
         differences.append(abs(len(globals()[list_input[i]][0])- len(globals()[list_input[i]][1])))
    
    for i in range(len(differences)): # n
        if len(B) < B_size:
            B.append(i)
        else:
            maxd = differences[B[0]] #biggest diff
            maxi = 0 #location of biggest diff
            for ii in range(len(B)): # m = size of B aka small af
                if maxd < differences[B[ii]]: #find biggest diff and index of biggest dif in B
                    maxd = differences[B[ii]]
                    maxi = ii
            if differences[i] < maxd:
                B[maxi] = i #replace biggest diff with current diff if smaller
                A.append(maxi)
            else:
                A.append(i)

    for i in range(len(A)):
        AA.append(list_input[A[i]])

    for i in range(len(B)):
        BB.append(list_input[B[i]])

    P = dict()
    # ##MY ADD##
    # AA = []
    # BB = []
    # for i in range(len(list_input)):
    #     if i < B_size:
    #         BB.append(list_input[i])
    #     else:
    #         AA.append(list_input[i])
    # ##TILL HERE MY ADD##
    P['A'] = AA
    P['B'] = BB
    return P


"""
compatabilityClasses will generate all the compatible classes to finding the Maximum Compatability Classes
PA a partitionGroup of PA sets
PB a partitonGroup of PB sets
Pf a partitionGroup of Pf sets
"""
def getCompatabilityClasses(PA, PB, Pf):
    PBp = []
    PBo = dict()
    PBt = []
    D = dict()
    D['P(A)'] = PA
    #print (range(1,len(PB)))
    for i in range(len(PB)-1):
        for ii in range(i+1,len(PB)):
            PBp = list(PB)
            PBp.append(PB[i].union(PB[ii]))
            del PBp[ii]
            del PBp[i]

            D['P(B'+str(i)+'_'+str(ii)+')'] = PBp
            #print (D)
            #print (i," and ",ii,": ",PBp)
            #print ("\n")
            #print (len(PB))
            #print ("D: ", D)
            #print ("\n")
            #PT = getPartitionGroup(['A','B'+str(i)+'_'+str(ii)],D)
            PT = getIntersections(D['P(A)'], D['P(B'+str(i)+'_'+str(ii)+")"])
            #print ("PT: ",PT)
            if(checkCompatability(PT, Pf)):
                PBo['P(B'+str(i)+'_'+str(ii)+')'] = PBp
                PBt.append((i, ii))


    return PBt
        

"""
checkCompatability will compare to sets to check if they are subsets of each other
P0 a partition 
P1 a partition
"""
def checkCompatability(P0, P1):

    interFound = 0;
    
    for i in P0:
      for ii in P1:
          if(i.issubset(ii)):
            interFound += 1

      if(interFound == 0):
        return 0
      else:
        interFound = 0

    return 1

    
