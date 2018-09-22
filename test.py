import itertools

list_input = ['x1','x2','x3']

d1 = {'P(x0)': [{0, 2}, {1, 2, 3}], 'P(x1)': [{0, 1, 2}, {0, 3}], 'P(y0)': [{0, 1, 2}, {3}]}

def function(n):
    for x in itertools.product(range(2),repeat=n):
        print (list(x)+[0,1,2])

function(3)

#for i in range(0,3):
#    globals()['variable{}'.format(i)] = i
#print (variable0)
        
