#!/usr/local/biotools/python/2.7.3/bin/python

from __future__ import division
import os
import argparse
import sys
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time

########################################################################################################
'''This programs parses processed fastq files to hash out the first 19 or 23 sequences from the reads'''
########################################################################################################

def ParseArgs():
    parser = argparse.ArgumentParser(description="Hashes out the first 19 or 23 sequences from fastq files")
    parser.add_argument("-f", dest="fastq_file", required=True, help="Fastq File")
    parser.add_argument("-o", dest="output_directory", required=True, help="The Output Directory for Results")
    args = parser.parse_args()

    fastq_file = os.path.abspath(args.fastq_file)
    output_path = os.path.abspath(args.output_directory)

    if output_path.endswith("/"):
        output_path = output_path
    else:
        output_path = os.path.abspath(args.output_directory) + "/"

    return(fastq_file, output_path)

def main():
    fastq_file, output_path = ParseArgs()
    hash_table = ParseFastq(fastq_file)
    result_file = Make_Result_File(output_path)

    result = open(result_file, "w")
    result.write("Sequence,Count\n")
    for sequence in hash_table:
        result.write(sequence + "," + str(hash_table[sequence]) + "\n")

    result.write("End of script\n")
    result.close()

    print("Script is done running")

def ParseFastq(fastq_file):
    hash_table = {}
    read_fastq_file = open(fastq_file).read().splitlines()

    for reads in read_fastq_file:
        sequence = reads[0:18]
        if sequence not in hash_table:
            hash_table[sequence] = 1
        else:
            hash_table[sequence] += 1

    return(hash_table)

def Make_Result_File(output_path):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    result_file = output_path + "ParseFastq_Results" + timestr + ".csv"

    return(result_file)
    

if __name__ == '__main__':
    main()