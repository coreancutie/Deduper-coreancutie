## Define the problem

There can be PCR duplicates after the sequencing, quality checking, and alignment of a sample. We want to remove these duplicates present in the SAM file after the alignment step, but we have to check a lot of different parameters before we can call something a PCR duplicate. We must ensure that the strands have the same alignment position: the same chromosome, the same 5' or left-most position (this includes accounting for soft clipping), and are the same strand (not a reverse complment of each other). Along with same alignment position, we must check if the strands have the same unique molecular identifer (UMI). In this case, I will only be accounting for single-end read, not pair-end reads. 

## Write examples:
    - Include a properly formated sorted input sam file
    - Include a properly formated expected output sam file

## pseudocode

```
Sort the SAM file using Samtools sort (will sort using the leftmost coordinate of the alignment: column 4)

Make a set of all known UMI

    Read the SAM file in

        Extract each line of the SAM file (readline)

            Seperate the line by tab and strip the newline

                Make a dictionary with the key as the column 1 (query name)

                Call the position function (to get the position accounting for the CIGAR string)

                The values are a list: [strand, chromosome, position]

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

Input:
Output:
```

```
def position_pos(column_4, column_6):

    '''Given the the left most position (column 4 from SAM) and the CIGAR string (column 6 SAM), I account for soft clipping if presnet and return the 5' start of read'''


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

    '''Given the the left most position (column 4 from SAM) and the CIGAR string (column 6 SAM), I account for soft clipping if presnet and return the 5' start of read'''


    soft_clip = 0

    for i in range(column_6):
        #seeing where there is a soft clip 'S' AND if its at the very end
        if column_6[i] == "S" and column_6[i] == column_6[-1]:
            soft_clip = column_6[:i]
            
    5_start = column_4 + soft_clip

    return(5_start)

Input: 10, 5S136M4S
Output: 14
```
