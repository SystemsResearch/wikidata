"""
Created by Dimitri Perrin, September 2022
"""

import glob, subprocess, datetime

# Input and output folders. Note: make sure you are using the correct folders
folder_in = "/work/wikidata/"
folder_out = "/work/wikidata/extracted_files/"

# List of files to process

# Hard-coded files
files = ["enwiki-20220201-pages-meta-history1.xml-p1p857.7z"]

# Alternatively, we can use `glob` to get a list of all files matching a pattern
#files = glob.glob("enwiki-20220201-pages-meta-history*.7z")



"""
Simple function to print a timestamped message

Parameters:
txt (string): message to display

Returns:
None
"""
def progress_message(txt):
    # datetime object containing current date and time
    now = datetime.datetime.now()
    # time, formatted as dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string,txt)



"""
Main part of the program.

Iterates over the list of files.
For each file, unzips it to the specified folder.
"""

progress_message(f"Starting. Number of files to process: {len(files)}")

for current_file in files:
        progress_message(f"Processing {current_file}")
        subprocess.call(["7za","-y","e",folder_in+current_file,"-o"+folder_out])

progress_message("Done.")
