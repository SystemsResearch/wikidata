#!/bin/bash -l

# declare a name for this job 
#PBS -N wiki_xml_process  

# request CPU(s)
#PBS -l ncpus=1

# request memory
#PBS -l mem=64G

# request time
#PBS -l walltime=2:00:00        

# mail is sent to you when the job starts and when it terminates or aborts
#PBS -m bea
# specify your email address
#PBS -M dimitri.perrin@qut.edu.au

# By default, PBS scripts execute in your home directory, not the 
# directory from which they were submitted. The following line 
# places you in the directory from which the job was submitted.  
cd $PBS_O_WORKDIR

# load the required modules (lxml and beautifulsoup)
module load beautifulsoup4/4.11.1-foss-2021b-python-3.9.6
module load lxml/4.6.3-gcccore-11.2.0

# run the program
python3.9 /home/perrin2/wikidata/xml_process_example.py
exit 0
