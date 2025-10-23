#!/usr/bin/env python

#need this import to use argparse variables
import argparse
def get_args():
	'''this has 1 arguement: sam file'''
	parser = argparse.ArgumentParser(description="Getting")
	parser.add_argument("-f", help="absolute file path to sorted sam file", type=str, required=True)
	parser.add_argument("-o", help="absolute file path to sorted sam file", type=str, required=True)
	parser.add_argument("-u", help="absolute path to file containing the list of UMIs", type=str, required=True)
	parser.add_argument("-h", help="prints a USEFUL help message and any assumptions your code", type=str, required=False)
	return parser.parse_args()

#calling the function (so in the terminal it runs)
args=get_args()

#reassiging args.sam filename as f
f:str = args.f

#reassiging args.output filename as o
o:str = args.o 

#reassiging args.sam filename as f
u:str = args.u

#reassiging args.output filename as o
h:str = args.h