__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from utils import *

def main():
    d = PARSE_PLA("PLA1")
    list_input = ['x2','x3','x0']
    P = getPartitionGroup(list_input,getPartition(d))
    list_output = ['y0','y1']
    Pf = getPartitionGroup(list_output,getPartition(d))
    print (P,Pf)

if __name__== "__main__":
  main()