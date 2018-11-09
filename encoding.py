"""
Return occurences in a dictionary with appended MCCS
i.e {0: [3, 4 ,5 ,7]} where 3 is the occurences
and 4,5,7 is the MCCS it occurs in
"""
def getOccurences(MCC, PB):
    occurs = {}
    for i in range(len(MCC)):
        for ii in MCC[i]:
            for j in PB[ii]:
                if j in occurs.keys():
                    occurs[j][0] += 1
                else:
                    occurs[j] = [1]
                occurs[j].append(i)
    return occurs

def encodeOccurs(occurs, MCC, gray_l, gray_c):
    MCC_enc = [0]*len(MCC)
    gray_f = [0]*len(gray_c)
    #gray_f = [1,0,0,0,0,0,0,0]
    z = []
    g_table = [0]*len(occurs)
    

    #print(MCC_enc)
    target = 2**(gray_l-1)
    while(target >= 0):
        for cube in occurs:
            if(occurs[cube][0]%2 != 0 and occurs[cube][0] != 1 and cube not in z):
                z.append(cube)
                continue

            if(occurs[cube][0] == target):
##                print(occurs[cube])
##                print("\n")
                temp_is_enc = []
                temp_not_enc = []
                for i in range(1,len(occurs[cube])): # through MCCs
                    if(MCC_enc[occurs[cube][i]]): # if MCC is encoded
                        temp_is_enc.append(occurs[cube][i])
                    else:
                        temp_not_enc.append(occurs[cube][i])
                #print("is enc",temp_is_enc)
                #print("nt enc",temp_not_enc)

                if(not temp_not_enc): #everything encoded
                    code = isAdj(MCC_enc[temp_is_enc[0]], temp_is_enc, target/2, MCC_enc)
                    if(not code): #check if differ by target/2
                        z.append(cube)
                    g_table[cube] = code
                    continue
                


                for CC in temp_not_enc: # have at it, go thru CCs
                    gotoZ = 1
                    for i in range(len(gray_c)): # go thru gray list
                        if(gray_f[i]): # continue if gray not available
                            continue
                        else:
                            code = isAdj(gray_c[i], temp_is_enc, target/2, MCC_enc)
                            if(code): 
                                MCC_enc[CC] = gray_c[i]
                                temp_is_enc.append(CC)
                                gray_f[i] = 1
                                g_table[cube] = code
                                gotoZ = 0
                                break
                            else:
                                continue
                    if(gotoZ):
                        z.append(cube)
                
                
        if(target == 0):
            target = -1
            
        target /= 2
    #print(MCC_enc)
    
    return MCC_enc, z, g_table

def isAdj(test, refs, diff_l, MCC_enc):
    if(not refs):
        return test
    else:
        res = test
        for ref in refs:
            for i in range(len(res)):
                if(res[i] == MCC_enc[ref][i]):
                    continue
                else:
                    res = res[:i] + '-' + res[i+1:]

        count = 0
        for c in res:
            if(c == '-'):
                count += 1

        if(count <= diff_l):
            return res
        else:
            return 0

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

def step1():
    
    expand()
