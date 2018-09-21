__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

from utils import *

def main():
    d = PARSE_PLA("PLA1")
    print (getPartition(d))

if __name__== "__main__":
  main()