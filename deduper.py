#!/usr/bin/env python

#need this import to use argparse variables
import argparse
def get_args():
	'''this has 1 arguement: sam file'''
	parser = argparse.ArgumentParser(description="Getting")
	parser.add_argument("-f", help="The absolute path to the sorted sam file", type=str, required=True)
	parser.add_argument("-o", help="The absolute path to the sorted sam file", type=str, required=True)
	parser.add_argument("-u", help="The absolute path to the file containing the list of UMIs", type=str, required=True)
	return parser.parse_args()

#calling the function (so in the terminal it runs)
args=get_args()

#reassiging args.sam filename as f
f:str = args.f

#reassiging args.output filename as o
o:str = args.o 

#reassiging args.sam filename as f
u:str = args.u


#creating an empty set to store all UMI records
UMI:set = set()

#opening the UMI file to read
with open(u, "r") as umi_file:
	#looping through each UMI line
    for line in umi_file:
        #stripping the line!
        line = line.strip("\n")
        #adding the UMI string to the set
        UMI.add(line)

print(UMI)

