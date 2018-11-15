import copy

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

def split(v):
    exp = []
    for i in range(len(v)):
        if v[i]==2:
            temp_v = v.copy()
            temp_v[i] = 0
            exp.append(temp_v.copy())
            temp_v[i] = 1
            exp.append(temp_v.copy())
    return exp
    

"""
Return occurences in a dictionary with appended MCCS
i.e {0: [3, 4 ,5 ,7]} where 3 is the occurences
and 4,5,7 is the MCCS it occurs in
"""
def getOccurences(MCC, PB, N_P):
    
    occurs = [[] for _ in range(N_P)]
    for i in range(len(MCC)):
        for ii in MCC[i]:
            for j in PB[ii]:
                if i in occurs[j]:
                    continue
                else:
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
        for cube in range(len(occurs)):
            if(len(occurs[cube])%2 != 0 and len(occurs[cube]) != 1 and cube not in z):
                z.append(cube)
                continue

            if(len(occurs[cube]) == target):
##                print(occurs[cube])
##                print("\n")
                temp_is_enc = []
                temp_not_enc = []
                for i in range(0,len(occurs[cube])): # through MCCs
                    if(MCC_enc[occurs[cube][i]]): # if MCC is encoded
                        temp_is_enc.append(occurs[cube][i])
                    else:
                        temp_not_enc.append(occurs[cube][i])
               # print("is enc",temp_is_enc)
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
    g_table_ret = str2lst(g_table, len(occurs))
    MCC_enc_ret = str2lst(MCC_enc, len(MCC_enc))
    return MCC_enc_ret, z, g_table_ret



def str2lst(d, length):
    list_ret = [[] for _ in range(length)]
    for i in range(len(d)):
        if d[i] == 0:
            continue
        else:
            for bit in (d[i]):
                   if bit == '0':
                        list_ret[i].append(0);
                   if bit == '1':
                        list_ret[i].append(1);
                   if bit == '-':
                        list_ret[i].append(2); 
    return list_ret

def step1(g_table, z, g_code):
    print("-----------STEP1--------------","\n")
    temp_z = copy.deepcopy(z)
    for cube in z:
        s = split(g_table[cube])
        for i in range(0,len(s),2):
            print(cube)
            if s[i] in g_table and s[i+1] in g_table:
                if(g_code[g_table.index(s[i])] and g_code[g_table.index(s[i+1])]):
                    temp_z.remove(cube)
                    g_table[cube] = []
    print("-----------STEP1---Done-----------","\n")  
    return temp_z
    
    
"""
Encoding Step 2
"""
def step2(z,prodCC,g_table,cc_code,g_code):
    print("-----------STEP2--------------","\n")
    print("Z Set:",z)
    print("Prod CCs:",prodCC)
    print("G table",g_table)
    g_table1 = copy.deepcopy(g_table)
    g_code1 = copy.deepcopy(g_code)
    z1 = copy.deepcopy(z)
    for i in z:
        subcubes = expand(g_table[i])
        subcode = []
        subcube = []
        for j in subcubes:
            for k in range(0,len(prodCC)):
                for l in prodCC[k]:
                    subcubes_prodcc = expand(l)
                    if(j in subcubes_prodcc):
                        subcode.append(cc_code[k])
                        subcube.append(j)
                       # print (i,j,">>>>",subcubes_prodcc,subcode,subcube)
        list2 = [x for x in subcode if x]
        subcode = list2
        if(len(subcode)==len(subcube)):
            g_table1[i] = subcube[0]
            g_code1[i] = subcode[0]
            for m in range(1,len(subcube)):
                #g_table1.update({len(g_table1) : subcubes[m]})
                g_table1.append(subcube[m])
                #g_code1.update({len(g_code1) : subcode[m]})
                g_code1.append(subcode[m])
            z1.remove(i)
    print("-----------STEP2---Done-----------","\n")  
    return z1,g_table1,g_code1


