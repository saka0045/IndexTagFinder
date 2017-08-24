# -*- coding: utf-8 -*-
#!/usr/local/biotools/python/2.7.3/bin/python
import sys
import re
import os
import argparse

"""
Created on Fri Nov  4 14:13:58 2016

@author: m006703
"""

def ParseArgs():
    parser = argparse.ArgumentParser(description="Takes an input strand and outputs the compliment and reverse compliment strand")
    parser.add_argument("-i", "--inputstrand", dest="inputStrand", required=True, help="The Input Strand")
    args = parser.parse_args()

    return args

def main():
    args = ParseArgs()
    ComplimentaryStrand, ReverseComplimentaryStrand = ShowReverseComplimentaryStrand(args.inputStrand)
    print("Complementary Strand is: " + ComplimentaryStrand)
    print("Reverse Complimentary Strand is: " + ReverseComplimentaryStrand)


def ShowReverseComplimentaryStrand(inputStrand):
    StrandHolder=inputStrand.replace("A","AR",len(inputStrand))
    StrandHolder=StrandHolder.replace("T","TR",len(StrandHolder))
    StrandHolder=StrandHolder.replace("C","CR",len(StrandHolder))
    StrandHolder=StrandHolder.replace("G","GR",len(StrandHolder))
    ComplimentaryStrand=StrandHolder.replace("AR","T",len(StrandHolder))
    ComplimentaryStrand=ComplimentaryStrand.replace("TR","A",len(ComplimentaryStrand))
    ComplimentaryStrand=ComplimentaryStrand.replace("CR","G",len(ComplimentaryStrand))
    ComplimentaryStrand=ComplimentaryStrand.replace("GR","C",len(ComplimentaryStrand))
    ReverseComplimentaryStrand=ComplimentaryStrand[::-1]

    return(ComplimentaryStrand, ReverseComplimentaryStrand)

if __name__ == '__main__':
    main()
