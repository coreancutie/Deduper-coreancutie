#!/bin/bash
#SBATCH --account=bgmp                      #REQUIRED: which account to use
#SBATCH --partition=bgmp                    #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                   #optional: number of cpus, default is 1
#SBATCH --mem=16GB                          #optional: amount of memory, default is 4GB per cpu
#SBATCH --mail-user=catcar@uoregon.edu      #optional: if you'd like email
#SBATCH --mail-type=ALL                     #optional: must set email first, what type of email you want
#SBATCH --job-name=deduper                  #optional: job name
#SBATCH --output=deduper%j.out              #optional: file to store stdout from job, %j adds the assigned jobID
#SBATCH --error=deduper%j.err               #optional: file to store stderr from job, %j adds the assigned jobID


#calling the function
/usr/bin/time -v ./carmosino_deduper.py -u /projects/bgmp/catcar/bioinfo/Bi624/Deduper-coreancutie/STL96.txt \
-f /projects/bgmp/catcar/bioinfo/Bi624/Deduper-coreancutie/sam_files/C1_SE_uniqAlign.sorted.sam  \
-o /projects/bgmp/catcar/bioinfo/Bi624/Deduper-coreancutie/test/C1_SE_uniqAlign_output.sorted.sam 