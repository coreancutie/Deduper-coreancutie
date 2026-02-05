# Deduper (PCR Deduplication)

**Prompt:** Given a SAM file of uniquely mapped reads, and a text file containing the known UMIs, remove all PCR duplicates (retain only a single copy of each read). 

The algorithm represented in this repository is deigned for for single-end data, with 96 unique UMIs. Any sequences are discarded if they have UMIs with errors (invalid or unknown). UMI information is the last section in the QNAME. In the example QNAME `NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT`, the UMI is `GAACAGGT`. 

## [Part 1](part1.md)
Write up a strategy for writing a Reference Based PCR Duplicate Removal tool. That is, given a sorted sam file of uniquely mapped reads, remove all PCR duplicates (retain only a single copy of each read). Develop a strategy that avoids loading everything into memory. This includes:
- Define the problem
- Write examples:
    - Include a properly formated sorted (by chromosome) [input sam file](test/test_input.sam)
    - Include a properly formated expected [output sam file](test/test_output.sam)
- Develop algorithm using pseudocode
- Determine high level functions
    - Description
    - Function headers
    - Test examples (for individual functions)
    - Return statement

## [Part 2](carmosino_deduper.py)
Write the deduper function!

This Python code assumes a sorted sam file as the input. These are the sametools commands used to sort the SAM file before running it though the script (if given a SAM, convert to BAM, then sort as a BAM, finally convert to SAM). 

- convert SAM to BAM

    `samtools view -bS input.sam -o output.bam`

- sort BAM by chromosome

    `samtools sort input.bam -o output.sorted.bam`

- convert BAM to SAM

    `samtools view -h input.bam > output.sam`

This algorithm accounts for:
- All possible CIGAR strings (including adjusting for soft clipping)
- Strand (positive ot negative)
- Single-end reads
- Left most start position
- Known UMIs

This algorithm:
- Is compatible in Python 3.12
- Outputs the first read encountered if duplicates are found
- Outputs a properly formatted SAM file

## Part 3
Considerations for future implementations:
- Single-end vs paired-end input files
- Known UMIs vs randomers
- Error correction of known UMIs
- Choice of duplicate written to file (first, random, highest quality score)

