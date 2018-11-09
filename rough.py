import copy
cube = [1,2,1,0]
sub= []
swap = []
for i in range(0,len(cube)):
    if(cube[i]==2):
        swap = copy.copy(cube)
        swap[i]=0
        sub.append(swap)
        swap1 = copy.copy(cube)
        swap1[i] = 1
        sub.append(swap1)
print (sub)