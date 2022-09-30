"""
Created by Dimitri Perrin, September 2022
"""


import glob, subprocess, datetime, ast
from bs4 import BeautifulSoup as bs


# Input and output folders. Note: make sure you are using the correct folders
folder_in = "/work/wikidata/extracted_files/"
folder_out = "/work/wikidata/extracted_files/"

# List of files to process

# Hard-coded files
files = ["enwiki-20220201-pages-meta-history1.xml-p1p857.notext", "enwiki-20220201-pages-meta-history17.xml-p22110007p22238459.notext"]

# Alternatively, we can use `glob` to get a list of all files matching a pattern
#files = glob.glob(folder_in+"*.notext")


def progress_message(txt):
"""
Simple function to print a timestamped message

Parameters:
txt (string): message to display

Returns:
None
"""
    # datetime object containing current date and time
    now = datetime.datetime.now()
    # time, formatted as dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # we print the time and the message
    print(dt_string,txt)



def extract_data(filename, folder):
"""
Function that reads from an XML file, extracts some data, and saves to CSV.
For this example, we extract timestamp and contributor

Parameters:
filename (string): full path to the XML file
folder (strong): full path to the output folder

Returns:
None
"""
        # first, we read the file
        with open(filename, "r") as inFile:
            # Read each line in the file, readlines() returns a list of lines
            content = inFile.readlines()
            # Combine the lines in the list into a string
            content = "".join(content)
            bs_content = bs(content, "lxml")
        
        progress_message(f"Data in memory. Parsing.")

        # we extract the pages
        pages = bs_content.find_all("page")
        progress_message(f"{len(pages)} pages to process")
        
        nb_page_processed = 0
        
        # hacky way to create the ouput file name
        temp_name = filename.split("/")[-1]
        output_name = temp_name+".csv"
        
        with open(folder+output_name,'w') as outFile:

            # header line
            outFile.write("Page ID,Page title,Revision ID,Timestamp,Contributor ID,Contributor name\n")

            # for each page
            for p in pages:
            
                # we extract the page title
                title = p.find("title")
                title_value = str(title)[7:-8]
                
                # we extract the page ID
                ID = p.find("id")
                ID_value = str(ID)[4:-5]
                            
                # we extract the revisions
                revisions = p.find_all("revision")
                
                # for each revision
                for r in revisions:
                    
                    # we extract the revision ID
                    rev_ID = r.find("id")
                    rev_ID_value = str(rev_ID)[4:-5]

                    # we extract the timestamp
                    rev_time = r.find("timestamp")
                    rev_time_value = str(rev_time)[11:-12]
                    
                    # we extract the contributor
                    contributor = r.find("contributor")
                    
                    # the contributor can be a registered user or an IP
                    contributor_ID = contributor.find("id")
                    if contributor_ID != None:
                        contributor_value = str(contributor_ID)[4:-5]
                        contributor_name = str(contributor.find("username"))[10:-11]
                        
                        # same usernames have commas, so we need to escape them
                        contributor_name = '"'+contributor_name+'"'
                    else:
                        contributor_IP = contributor.find("ip")
                        contributor_value = str(contributor_IP)[4:-5]
                        contributor_name = "N/A"

                    outFile.write(f"{ID_value},{title_value},{rev_ID_value},{rev_time_value},{contributor_value},{contributor_name}\n")


                nb_page_processed+=1
                # we show how much progress has been made
                if nb_page_processed % 100 == 0:
                    progress_message(f"Processed {nb_page_processed} pages")



"""
Main part of the program.

Iterates over the list of files.
For each file, extracts data and saves to CSV.
"""

progress_message(f"Starting. Number of pages to process: {len(files)}")

for current_file in files:
        progress_message(f"Processing file {current_file}")
        extract_data(folder_in+current_file,folder_out)

progress_message("Done.")
