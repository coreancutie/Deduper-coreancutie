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

#importing regular expression (regex)
import re

#creating an empty set to store all UMI records
UMI:set = set()

#opening the UMI file to read
with open(u, "r") as umi_file:
	#looping through each UMI line
    for line in umi_file:
        #stripping the line of newline
        line = line.strip("\n")
        #adding the UMI string to the set
        UMI.add(line)


#assigning the chromosome to 1 initally (in a sorted SAM it should be 1 first.... right?)
chromosome:int = 1

#creating an empty set to store all reads (each read will be a tuple?, string? of the read items)
read:set = set()

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
                #writing the header line to the output file
                output.write("\t".join(line))
                #writing a new line because I can't merge it to the other write statement right now lol
                output.write("\n")
            #if the line is not a header
            else:
                # print(line[2])
                while int(line[2]) == chromosome:
                    print(line)
                    break
            #         Make a dictionary with the key as the whole line
            #         The values are a list of [UMI, strand, position]

            #         Extract the UMI from the first column

            #         if UMI not in known UMI set:
            #             throw that read away and go to next line in SAM file
            #             continue

            #         elif UMI is in the known UMI set:
            #             add UMI to dictionary value list
                            
            #             Call the strand function to determine if pos or neg strand
            #             Add strand (column 2) to the dictionary

            #             if pos(false):
                            
            #                 Call the pos position function to get the position accounting for the CIGAR string

            #                 Add position to the dictionary

            #             elif neg(true):
                            
            #                 Call the neg position function to get the position accounting for the CIGAR string

            #                 Add position to the dictionary
                
            #     Now outside of the while loop (completed getting all info for each chromosome)
            #     Compare each dictionary value to the others
            #         once there is a pcr duplicate write the first entry to the file and move on to the next
                
            #     empty the dictionary (reinitalize an empty one)
            #     chrom += 1 (incrementing the chromomosome)



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