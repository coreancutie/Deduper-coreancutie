# Deduper: PCR Deduplication Script

**Overview:** Given a SAM file of uniquely mapped reads, and a text file containing the known UMIs, remove all PCR duplicates. The final file will retain only a single copy of each read. 

The algorithm represented in this repository is deigned for for single-end data, with 96 unique UMIs. Any sequences are discarded if they have UMIs with errors (invalid or unknown). UMI information is the last section in the QNAME. In the example QNAME `NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT`, the UMI is `GAACAGGT`. 

## [Part 1](part1.md)
Writing a strategy for a Reference-Based PCR Duplicate Removal tool that avoids loading everything into memory. This includes:
- Defining the problem
- Writing examples:
    - Properly formatted sorted (by chromosome) [input sam file](test/test_input.sam)
    - Properly formatted expected [output sam file](test/test_output.sam)
- Developing algorithm using pseudocode
- Outlining high level functions
    - Description
    - Function headers
    - Test examples (for individual functions)
    - Return statement

## [Part 2](carmosino_deduper.py)
Write the deduplication function.

This Python code assumes the input is a sorted sam file. These are the sametools commands used to sort the SAM file before supplying though the deduplication script. 

- convert SAM to BAM

    `samtools view -bS input.sam -o output.bam`

- sort BAM by chromosome

    `samtools sort input.bam -o output.sorted.bam`

- convert BAM to SAM

    `samtools view -h input.bam > output.sam`

This algorithm accounts for:
- All possible CIGAR strings (including adjusting for soft clipping)
- Strand (positive or negative)
- Single-end reads
- Left most start position
- Known UMIs

This algorithm:
- Is compatible in Python 3.12
- Outputs the first read encountered if duplicates are found
- Outputs a properly formatted SAM file

Considerations for future implementations:
- Single-end vs paired-end input files
- Known UMIs vs randomers
- Error correction of known UMIs
- Choose which read to include/write in the final output:
    - First read in the input file
    - Choose a random read from the duplicates
    - Keep the read with the highest quality score

