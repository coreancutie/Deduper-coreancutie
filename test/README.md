# Deduper Test File

## Input File - SAM

Line 25 & 26:
- A PCR duplicate (everything matched from the get go)

Line 27
- Has invald UMI

Line 28 & 29
- Not a PCR duplicate, different starting position

Line 30 & 31
- Not a PCR duplicate, different strand

Line 32 & 33
- A PCR duplicate that has different leftmost starting positions (but from soft clipping it is the same, POSITIVE STRAND)

Line 34 & 35
- Not a PCR duplicate, one of them had an invalid UMI

Line 36 & 37
- Not a PCR duplicate, they are on different chromosomes

Line 38 & 39
- A PCR duplicate that has different leftmost starting positions (but from soft clipping it is the same, NEGATIVE STRAND)

Line 40 & 41
- Not a PCR duplicate, after soft clipping the position changed

Line 42 & 43
- Not a PCR duplicate, they have different UMI (both valid)

## Output File

Contains all of the headers which are unchanged. 

Kept the line 25 from input (A PCR duplicate (everything matched from the get go)). 

Kept both line 28 & 29 from input (Not a PCR duplicate, different starting position)

Kept both line 30 & 31 from input (Not a PCR duplicate, different strand)

Kept line 32 from input (A PCR duplicate that has different leftmost starting positions (but from soft clipping it is the same, POSITIVE STRAND))

Kept both line 34 & 35 from input (Not a PCR duplicate, one of them had an invalid UMI)

Kept both line 36 & 37 from input (Not a PCR duplicate, they are on different chromosomes)

Kept line 38 from input (A PCR duplicate that has different leftmost starting positions (but from soft clipping it is the same, NEGATIVE STRAND))

Kept line 40 & 41 from input (Not a PCR duplicate, after soft clipping the position changed)

Kept line 42 & 43 from input (Not a PCR duplicate, they have different UMI (both valid))
