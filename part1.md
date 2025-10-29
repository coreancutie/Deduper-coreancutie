## Define the problem

There can be a phenominom called a PCR duplicates which is something that can occur after the sequencing, quality checking, and alignment of a sample. These duplicates are present in a SAM or BAM file. Before moving on with the data, it is recomended to remove these duplicates present in the file specifically after the alignment step. In order to remove a PCR duplicate, several parameters need to be checked in order to identify a proper PCR duplicate. These parameters are:

1. We must ensure that the reads have the same strand (neg or pos).
2. The reads are on the same chromosome. 
3. The reads have the same 5' start position or left-most position (this includes accounting for soft clipping). 
4. The reads have the same known unique molecular identifer (UMI). 
git
In this code, single-end read is all that is acocunted for. Pair-end reads will not work on this algorithum.

## Write test files for an example:
    - Include a properly formated sorted input sam file
    - Include a properly formated expected output sam file

## Write pseudocode:

```
Sort the SAM file using Samtools sort (will sort using the chromosome: column 3)

---

Create an empty set for known UMI

Read in the UMI txt file:

    read each line in the file

        strip the newline

        add each line (UMI) to the set of known UMI's

---

initalizing chrom = 0
initalizing empty dictionary = {}

Open a file for writing the new SAM file:

    Open the SAM file to read:

        Extract each line of the SAM file (readline):

            Seperate the line by tab and strip the newline

            check if the line is a header: (if line[0][0] == "@")

                Write the header line to the new file

            if the line is not a header: (else)

                while the chromosome (column 3) is the same to the one initalized: 

                    Make a dictionary with the key as the whole line
                    The values are a list of [UMI, strand, position]

                    Extract the UMI from the first column

                    if UMI not in known UMI set:
                        throw that read away and go to next line in SAM file
                        continue

                    elif UMI is in the known UMI set:
                        add UMI to dictionary value list
                            
                        Call the strand function to determine if pos or neg strand
                        Add strand (column 2) to the dictionary

                        if pos(false):
                            
                            Call the pos position function to get the position accounting for the CIGAR string

                            Add position to the dictionary

                        elif neg(true):
                            
                            Call the neg position function to get the position accounting for the CIGAR string

                            Add position to the dictionary
                
                Now outside of the while loop (completed getting all info for each chromosome)
                Compare each dictionary value to the others
                    once there is a pcr duplicate write the first entry to the file and move on to the next
                
                empty the dictionary (reinitalize an empty one)
                chrom += 1 (incrementing the chromomosome)
                
```


## High level functions:

```
def strand(column_2):

    '''Given the bitwise FLAG (column 2) in the SAM file, I return if the strand is the positive(False) or negative (True)'''

    #THIS IS POS/FOWARD STRAND
    rev_comp = False

    #THIS IS NEG/REVERSE STRAND
    if ((flag & 16) == 16):
        rev_comp = True

    return(rev_comp)

Input: 82
Output: True
```

```
def position_pos(column_4, column_6):

    '''Given the the left most position (column 4 from SAM) and the CIGAR string (column 6 SAM), I account for soft clipping if present and return the 5' start of read'''


    soft_clip = 0

    for i in range(column_6):
        #seeing where there is a soft clip 'S' AND if its not at the very end
        if column_6[i] == "S" and column_6[i] != column_6[-1]:
            soft_clip = column_6[:i]
            
    5_start = column_4 - soft_clip

    return(5_start)

Input: 10, 5S136M4S
Output: 5
```

```
def position_neg(column_4, column_6):

    '''Given the the left most position (column 4 from SAM) and the CIGAR string (column 6 SAM), account for soft clipping if present and since it is a reverse strand I  and return the 5' start of read'''


    Find the M, D, and N, and add all of those values to column_4

    soft_clip = 0

    for i in range(column_6):
        #seeing where there is a soft clip 'S' AND if its at the very end
        if column_6[i] == "S" and column_6[i] == column_6[-1]:
            soft_clip = column_6[:i]
            
    5_start = column_4 + soft_clip

    return(5_start)

Input: 10, 5S155M5S
Output: 170
```
