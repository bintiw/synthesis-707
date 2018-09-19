__author__ = "Binayak Tiwari"
__version__ = "1.0.1"
__maintainer__ =  "Binayak Tiwari"
__email__ = "binayaktiwari@gmail.com"

import re

def PARSE_PLA(_PLA_FILENAME):
            PLA_COMMENT = re.compile(r"^#(.*$)")
            PLA_TYPE = re.compile(r'^.type\s+(f|r|fr|fd|dr|fdr)$') 
            PLA_INP= re.compile(r'^.i\s+((\d)+)$')
            PLA_OUT= re.compile(r'^.o\s+((\d)+)$')
            PLA_ILB = re.compile(r'^.ilb\s+((\w+\s?)+)\s?$')
            PLA_OB= re.compile(r'^.ob\s+((\w+\s?)+)\s?$')
            PLA_P= re.compile(r'^.p\s+((\d)+)$')
            PLA_TT= re.compile(r"^([01-]+)\s+([01-]+)$")
            PLA_CODE = {'0':0, '1':1, '-':2}
            PLA_TYPE_INT = {'f':0,'r':1,'fr':2,'fd':3,'dr':'4','fdr':5}


            f = open(_PLA_FILENAME,"r")
            s = f.readlines()

            d = dict(N_IP=None, N_OP=None,IP_LABEL=None, OP_LABEL=None,N_P=None, TYPE=None, TT=set())
            error = 0
            for lines in s:
                #print (lines)
                catch_TYPE = PLA_TYPE.match(lines)
                if(catch_TYPE):
                    try:
                        type_int = tuple(PLA_TYPE_INT[c] for c in catch_TYPE.groups() )
                        d['TYPE'] = int(type_int[0])
                        #print("TYPE:",type_int)
                    except Exception:
                        print("Error in .type description")
                        error = 1

                catch_INP = PLA_INP.match(lines)
                if(catch_INP):
                    try:
                        d['N_IP'] = int(catch_INP.group(1))
                        #print("Input:",catch_INP.group(1))
                    except Exception:
                        print("Error in .i description")
                        error = 1

                catch_OUT = PLA_OUT.match(lines)
                if(catch_OUT):
                    try:
                        d['N_OP'] = int(catch_OUT.group(1))
                        #print("Output",catch_OUT.group(1))
                    except Exception:
                        print("Error in .o description")
                        error = 1

                catch_COMMENT = PLA_COMMENT.match(lines)
                if(catch_COMMENT):
                    try:
                        print("Comment:",catch_COMMENT.group(1))
                    except Exception:
                        print("Error in writing comment")
                        error = 1

                catch_ILB = PLA_ILB.match(lines)
                if(catch_ILB):
                    try:
                        d['IP_LABEL'] = catch_ILB.group(1).split()
                        #print("Ip Signals:",catch_ILB.group(1))
                    except Exception:
                        print("Error in .ilb description")
                        error = 1

                catch_OB = PLA_OB.match(lines)
                if(catch_OB):
                    try:
                        d['OP_LABEL'] = catch_OB.group(1).split()
                        #print("Op Signals:",catch_OB.group(1))
                    except Exception:
                        print("Error in .ob description")
                        error = 1
                
                catch_P = PLA_P.match(lines)
                if(catch_P):
                    try:
                        d['N_P'] = int(catch_P.group(1))
                        #print("Row in TT:",catch_P.group(1))
                    except Exception:
                        print("Error in .p description")
                        error = 1

                catch_TT = PLA_TT.match(lines)
                if(catch_TT):
                    try:
                        ip , op = catch_TT.groups()
                        inp_ = tuple(PLA_CODE[c] for c in ip)
                        out_ = tuple(PLA_CODE[c] for c in op)
                        d['TT'].add((inp_,out_))
                        #print(inp_, out_)
                    except Exception:
                        print("Error in Truth Table description")
                        error = 1

            #print (d)
            if (len(d['IP_LABEL']) != d['N_IP']):
                print("Error in lenght of input and input labels, .i and .ilb description.")
                return (0)

            elif (len(d['OP_LABEL']) != d['N_OP']):
                print("Error in lenght of output and output labels, .o and .ob description")
                return (0)
            else:
                if error == 0:
                    return (d)
