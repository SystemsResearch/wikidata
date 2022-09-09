"""
Created by Dimitri Perrin, September 2022
"""


import glob, subprocess, datetime, ast

# Input and output folders. Note: make sure you are using the correct folders
folder_in = "/work/wikidata/"
folder_out = "/work/wikidata/extracted_files/"

# List of files to process

# Hard-coded files
files = ["enwiki-20220201-pages-meta-history1.xml-p1p857.7z", "enwiki-20220201-pages-meta-history17.xml-p22110007p22238459.7z"]

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
    # we print the time and the message
    print(dt_string,txt)



"""
Function that extracts from an XML file everything but the text of the pages

Parameters:
filename (string): full path to the XML file
folder (strong): full path to the output folder

Returns:
None
"""
def extract_XML(filename, folder):
    with open(filename,'r') as inFile, open(f"{filename}.notext",'w') as outFile:
        skip = False
        nb_page_processed = 0
        for line in inFile:
            # if we are currently skipping text...
            if skip:
                # ... and we reach the end of the text, we stop skipping
                if line.rstrip()[-7:] == "</text>":
                      skip = False
            # otherwise
            else:
                # if we see text, we start skipping
                if line.lstrip()[:5] == "<text":
                    skip = True
                # and if not, we keep writing to the file
                else:
                    outFile.write(line)
                    # we also keep count of the number of pages processed
                    if line.lstrip()[:6] == "<page>":
                        nb_page_processed+=1
                        # we show how much progress has been made
                        if nb_page_processed % 100 == 0:
                            progress_message(f"Processed {nb_page_processed} pages")

                


"""
Main part of the program.

Iterates over the list of pages.
For each page, finds the correct archive, unzips it, and extracts data for that page.
"""

progress_message(f"Starting. Number of pages to process: {len(files)}")

for current_file in files:
        
        # first, we unzip the file
        progress_message(f"Extracting file {current_file}")
        subprocess.call(["7za","-y","e",folder_in+current_file,"-o"+folder_out])
        
        # the resulting file has the same name, without the .7z extension
        # next, we extract the content
        progress_message(f"Extracting XML content")
        unzipped_file = folder_out+current_file[:-3]
        extract_XML(unzipped_file,folder_out)

        # finally, we delete the initial XML as we are no longer using it
        progress_message(f"Deleting file {unzipped_file}")
        subprocess.call(["rm",unzipped_file])

progress_message("Done.")
