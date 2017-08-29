#!/usr/local/biotools/python/2.7.3/bin/python

from __future__ import division
import os
import argparse
import sys
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time


###########################################################
'''
This program will look for the UPS Tag used in INDEXTESTING
'''
###########################################################

def main():
    run_path, config_file, output_path = ParseArgs()
    sample_list, sample_path = Find_Samples(run_path)
    forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment = Parse_Config_File(
        config_file)
    result_file = Make_Result_File(output_path)

    print(sample_list)
    print(str(len(sample_list)) + " total samples to process")
    result = open(result_file, 'w')
    result.write("Run: " + run_path + "\n")
    result.write("Sample,Total Reads,UPS Tag Reads,Percent\n")
    for sample in sample_list:
        fastq_files, fastq_path = Find_Fastq_Files(sample_path, sample)
        total_count, ups_tag_count, ups_tag_percent = Process_Fastq_Files(fastq_path, fastq_files, forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment)
        print(sample_path)
        print(fastq_path)
        print(fastq_files)
        print(total_count, ups_tag_count, ups_tag_percent)
        print("Percent of UPS tag reads is: " + str("%.2f" % ups_tag_percent) + "%" + " for sample " + sample)
        result.write(sample + "," + str(total_count) + "," + str(ups_tag_count) + "," + str(ups_tag_percent) + "\n")

    print("Script is done running")
    result.write("End of report\n")
    result.close()

def ParseArgs():
    parser = argparse.ArgumentParser(description="Looks to see if the UPS Tags in INDEXTESTING is present in a fastq file")
    parser.add_argument("-r", dest="run_directory", required=True, help="The Run Directory")
    parser.add_argument("-c", dest="config", required=True, help="Config File for Index Tag Finder")
    parser.add_argument("-o", dest="output_directory", required=True, help="The Output Directory for Results")
    args = parser.parse_args()

    run_path = os.path.abspath(args.run_directory)
    config_file = os.path.abspath(args.config)
    output_path = os.path.abspath(args.output_directory)

    if run_path.endswith("/"):
        run_path = run_path
    else:
        run_path = os.path.abspath(args.run_directory)+"/"

    if output_path.endswith("/"):
        output_path = output_path
    else:
        output_path = os.path.abspath(args.output_directory) + "/"

    return(run_path, config_file, output_path)

def Find_Samples(run_path):
    sample_path = run_path + "samples/"
    sample_list=[]
    for sample in os.listdir(sample_path):
        if sample == "lane1":
            continue
        else:
            sample_list.append(sample)

    return(sample_list, sample_path)

def Find_Fastq_Files(sample_path, sample):
    fastq_path = sample_path + sample + "/"
    fastq_files = []
    for file in os.listdir(fastq_path):
        if file.endswith(".fastq.gz"):
            fastq_files.append(file)

    return(fastq_files, fastq_path)

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

def Process_Fastq_Files(fastq_path, fastq_files, forward_tag, forward_tag_reverse_compliment, reverse_tag, reverse_tag_reverse_compliment):
    total_count = 0
    ups_tag_count = 0
    for file in fastq_files:
        Cmd = "zcat " + fastq_path + file + " | wc -l"
        total_output = Popen(Cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        count = int(total_output.stdout.read().strip())//4
        total_count += count
        Cmd = "zcat " + fastq_path + file + " | grep -E '" + forward_tag + "|" + forward_tag_reverse_compliment + "|" + reverse_tag + "|" + reverse_tag_reverse_compliment + "' | wc -l"
        tag_output = Popen(Cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        tag_count = int(tag_output.stdout.read().strip())
        ups_tag_count += tag_count
    try:
        ups_tag_percent = (ups_tag_count/total_count) * 100
    except ZeroDivisionError:
        ups_tag_percent = 0

    return(total_count, ups_tag_count, ups_tag_percent)

def Make_Result_File(output_path):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    result_file = output_path + "IndexTagFinder_Results" + timestr + ".csv"

    return(result_file)

if __name__ == '__main__':
    main()
