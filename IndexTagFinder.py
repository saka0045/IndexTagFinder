#!/usr/local/biotools/python/2.7.3/bin/python

from __future__ import division
import os
import argparse
import sys
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT


###########################################################
'''
This program will look for the UPS Tag used in INDEXTESTING
'''
###########################################################

def ParseArgs():
    parser = argparse.ArgumentParser(description="Looks to see if the UPS Tags in INDEXTESTING is present in a fastq file")
    parser.add_argument("-s", dest="sample_directory", required=True, help="The Sample Directory")
    parser.add_argument("-c", dest="config", required=True, help="Config File for Index Tag Finder")
    args = parser.parse_args()

    sample_path = os.path.abspath(args.sample_directory)
    config_file = os.path.abspath(args.config)

    if sample_path.endswith("/"):
        sample_path = sample_path
    else:
        sample_path = os.path.abspath(args.sample_directory)+"/"

    return(sample_path, config_file)

def main():
    sample_path, config_file = ParseArgs()
    fastq_files = Find_Fastq_Files(sample_path)
    forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment = Parse_Config_File(config_file)
    total_count, ups_tag_count, ups_tag_percent = Process_Fastq_Files(sample_path, fastq_files, forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment)
    print(sample_path)
    print(fastq_files)
    print(forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment)
    print(total_count, ups_tag_count, ups_tag_percent)
    print("Percent of UPS tag reads is: " + str("%.2f" % ups_tag_percent) + "%")

def Find_Fastq_Files(sample_path):
    fastq_files = []
    for file in os.listdir(sample_path):
        if file.endswith(".fastq.gz"):
            fastq_files.append(file)

    return(fastq_files)

def Parse_Config_File(config_file):
    config_file = open(config_file, 'r')
    config_dict = {}
    for each_line in config_file:
        if "=" not in each_line:
            continue
        each_line_split = each_line.split("=")
        config_dict[each_line_split[0]] = each_line_split[1].strip()
    config_file.close()

    return(config_dict["forward_tag"], config_dict["forward_tag_reverse_compliment"], config_dict["reverse_tag"], config_dict["reverse_tag_reverse_compliment"])

def Process_Fastq_Files(sample_path, fastq_files, forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment):
    total_count = 0
    ups_tag_count = 0
    for file in fastq_files:
        Cmd = "zcat " + sample_path + file + " | wc -l"
        total_output = Popen(Cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        count = int(total_output.stdout.read().strip())//4
        total_count += count
        Cmd = "zcat " + sample_path + file + " | grep -E '" + forward_tag + "|" + forward_tag_reverse_compliment + "|" + reverse_tag + "|" + reverse_tag_reverse_compliment + "' | wc -l"
        tag_output = Popen(Cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        tag_count = int(tag_output.stdout.read().strip())
        ups_tag_count += tag_count
    ups_tag_percent = (ups_tag_count/total_count) * 100

    return(total_count, ups_tag_count, ups_tag_percent)

if __name__ == '__main__':
    main()
