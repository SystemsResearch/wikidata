# declare a name for this job 
#PBS -N job_01  

# request CPU(s)
#PBS -l ncpus=1

# request memory
#PBS -l mem=64G

# request time
#PBS -l walltime=0:20:00        

# mail is sent to you when the job starts and when it terminates or aborts
#PBS -m bea
# specify your email address
#PBS -M dimitri.perrin@qut.edu.au

# By default, PBS scripts execute in your home directory, not the 
# directory from which they were submitted. The following line 
# places you in the directory from which the job was submitted.  
cd $PBS_O_WORKDIR

# run the program
python3.6 /home/perrin2/wikidata/unzip_and_extract_based_on_IDs.py
exit 0
