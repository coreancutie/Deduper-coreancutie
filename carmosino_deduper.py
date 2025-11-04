#!/usr/bin/env python

#need this import to use argparse variables
import argparse
def get_args():
	'''this has 1 arguement: sam file'''
	parser = argparse.ArgumentParser(description="Getting")
	parser.add_argument("-u", help="The absolute path to the file containing the list of UMIs", required=True)
	parser.add_argument("-f", help="The absolute path to the sorted sam file", required=True)
	parser.add_argument("-o", help="The absolute path to the sorted sam file", required=True)
	return parser.parse_args()

#calling the function (so in the terminal it runs)
args=get_args()

#reassiging args.sam filename as f
u:str = args.u
#reassiging args.sam filename as f
f:str = args.f
#reassiging args.output filename as o
o:str = args.o 

#importing regular expression (regex)
import re

#creating an empty set to store all UMI records
known_UMIs:set = set()

#opening the UMI file to read
with open(u, "r") as umi_file:
	#looping through each UMI line
    for line in umi_file:
        #stripping the line of newline
        line = line.strip("\n")
        #adding the UMI string to the set
        known_UMIs.add(line)

def strand(bit_flag:int) -> bool:

    '''Given the bitwise FLAG (column 2) in the SAM file, 
    this returns if the strand is the positive(False) or negative (True)'''

    #THIS IS POS/FOWARD STRAND
    rev_comp = False

    #THIS IS NEG/REVERSE STRAND
    if ((bit_flag & 16) == 16):
        rev_comp = True

    return(rev_comp)

# print(strand(0))
# print(strand(82))


def pos_5(LMP:int, CIGAR:str, strand:bool) -> int:

    '''Given the the left most position (column 4 from SAM) and the 
    CIGAR string (column 6 SAM), and the strand (column 2) (False for pos) (True for neg),
    I account for soft clipping if present and return the 5' start of read'''

    #assigning the inital shift for positive strand
    shift_pos = 0
    #assigning the inital shift for negative strand 
    shift_neg = 0

    #finding the M, N, D, and S, in the CIGAR STRING
    #findall returns any match as list of each element EX: ['5S', '136M', '4S']
    match = re.findall(r"[0-9]+[MNDS]+", CIGAR)
    
    #if true, if there is a match (there always should be...)
    if match:
        #looping through range of list of matches (i is 0, 1, 2, ...)
        for i in range(len(match)):
            #checking if the first instance is softclipping
            if i == 0 and "S" in match[i]:
                #adding the number associated with that CIGAR element for pos strand
                shift_pos += int(match[i][:-1])
            else:
                #adding the number associated with that CIGAR element for neg strand
                shift_neg += int(match[i][:-1])
    
    #if true (neg strand)
    if strand:
        #adding all the CIGAR elements to the left most position to get the 5' start position
        start_5 = LMP + shift_neg
    #if not true (pos strand)
    elif not strand:
        #subtract the soft clipped element from the left most position to get the 5' start position
        start_5 = LMP - shift_pos
    
    #returning the 5' start position
    return(start_5)

# print(pos_5(10, '5S136M4S', False)) # should retrun 5
# print(pos_5(10, "5S136M8I4S", True)) # this should return 150 


#assigning the chromosome to nothing initally
chromosome:str = ' '

#creating an empty set to store all reads (each item in the set will be a tuple of the umi, strand, 5' start pos, and chromosome)
read:set = set()

#setting a counter for amount of header lines
header_lines:int = 0
#setting a counter for amount of unique reads
unique_reads:int = 0
#setting a counter for amount of wrong/invalid/unknown UMIs
wrong_umi:int = 0
#setting a counter for amount of PCR duplicates removed
dup_removed:int = 0
#setting a dictionary to count the amount of reads per chromosome
num_per_chrom:dict = {}
#setting a variable to count the amount of reads per chromosome
num_in_chrom:int = 0

#opening the input file to read
with open(f, "r") as input:
    #opening the output file to write
    with open(o, "w") as output:
        #for line in the input
        for line in input:
            #stripping the line of new line and splitting by tab
            line = line.strip("\n").split("\t")

            #checking if the line is a header
            if line[0][0] == "@":
                #incrementing the header line count
                header_lines += 1
                #writing the header line to the output file
                output.write("\t".join(line))
                #writing a new line because I can't merge it to the other write statement right now lol
                output.write("\n")
            
            #if the line is not a header
            else:
                #if the chromosome in the line is not what is set:
                if line[2] != chromosome:
                    #creating a dictionary with the chromosome number as the key
                    #and the number of reads in that chromosome as the value
                    num_per_chrom[chromosome] = num_in_chrom

                    #setting the chromosome to that value
                    chromosome = line[2]

                    #resetting the chromosome count
                    num_in_chrom = 0
                    #resetting the read sets
                    read = set()

                #if the chromosome line is what is set, then get all the calculations:
                if line[2] == chromosome:
                    #getting the UMI from the first column (header) it should be the last 8 characters
                    umi = line[0][-8:]

                    #if the umi is not a valid or known
                    if umi not in known_UMIs:
                        #incrementing the wrong umi counter
                        wrong_umi += 1
                        #since it is not a known umi I go onto the next line in the file
                        continue

                    #if the umi is valid or known
                    elif umi in known_UMIs:

                        #getting the strand 
                        str = strand(int(line[1]))

                        #getting the 5' start position
                        start_pos = pos_5(int(line[3]), line[5], str)

                        #adding the umi, strand, 5' start position, and chromosome to a tuple
                        dup:tuple = (umi, str, start_pos, line[2])
                    

                        #if the information is not in read (it's not a PCR duplicate)
                        if dup not in read:
                            #incrementing the unique read counts
                            unique_reads += 1
                            #incrementing the number of read in that chromosome counter
                            num_in_chrom += 1
                            #writing the line to the output file
                            output.write("\t".join(line))
                            #writing a new line
                            output.write("\n")
                            #adding the information to the read to compare in the future
                            read.add(dup)

                        #if the information is in the read (its a PCR duplicate)
                        elif dup in read:
                            #incrementing the counter for duplcates removed
                            dup_removed += 1
                            continue
                        
#printing out the values
print(f"The number of header lines: {header_lines}")
print(f"The number of unique reads: {unique_reads}")
print(f"The number of wrong UMI: {wrong_umi}")
print(f"The number of PCR duplicates removed: {dup_removed}")

#writing out a file for all of the chromosome and their counts
with open(f"num_per_chrom.tsv", "w") as out_file:
    for key, value, in num_per_chrom.items():
        out_file.write(f"{key}\t{value}\n")
