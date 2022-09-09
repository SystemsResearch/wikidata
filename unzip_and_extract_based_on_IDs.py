"""
Created by Dimitri Perrin, September 2022
"""


import glob, subprocess, datetime, ast

# Input and output folders. Note: make sure you are using the correct folders
folder_in = "/work/wikidata/"
folder_out = "/work/wikidata/extracted_files/"

# List of page IDs to process
pages = [264, 198332, 35458904]


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
Function finding which file a given page comes from

Parameters:
page_ID (int): ID for the page we want to extract

Returns:
file (string): full path to the file containing that page
"""
def find_file(page_ID):
    # we get
    files = glob.glob(folder_in+"enwiki-20220201-pages-meta-history*.7z")
    for file in files:
        # filenames are structued like this:
        # enwiki-20220201-pages-meta-history13.xml-p9940247p10047273.7z
        
        # we extract the range of IDs
        range_ID = file.rstrip().split("-")[-1][1:-3]
        first_ID, last_ID = range_ID.split("p")
        
        # we convert the first and last IDs to numbers
        first_ID = ast.literal_eval(first_ID)
        last_ID = ast.literal_eval(last_ID)
        
        # if page_ID is between the two, we have found the file
        if page_ID>=first_ID and page_ID<=last_ID:
            return file



"""
Function that extracts from an XML file just the content we need for a given page

Parameters:
page_ID (int): ID for the page we want to extract
filename (string): full path to the XML file
folder (strong): full path to the output folder

Returns:
None
"""
def extract_XML(page_ID, filename, folder):
# note: the structure is <page>, then <title> on next line, then <ns> then <id>
    with open(filename,'r') as inFile, open(f"{folder}{page_ID}.xml",'w') as outFile:
        flag = False
        count = 0
        for line in inFile:
            # we are reaching a new page, so we start a counter
            if line.lstrip()[:6] == "<page>":
                count = 1
            # we save the title line in case we need it
            elif line.lstrip()[:7] == "<title>":
                title = line
                count+=1
            # we save the ns line in case we need it
            elif line.lstrip()[:4] == "<ns>":
                ns = line
                count+=1
            # we check the ID
            elif line.lstrip()[:4] == "<id>":
                if count==3: #revisions also have IDs, so we need to be careful
                    # we extract the ID (using strip rather than lstrip now, to handle the end-of-line character)
                    current_ID = ast.literal_eval(line.strip()[4:-5])
                    # if it is our page of interest...
                    if current_ID == page_ID:
                        page_name = title.strip()[7:-8]
                        progress_message(f"Saving page {page_name}")
                        # we write the title, ns, and current lines
                        outFile.write("<page>\n")
                        outFile.write(title)
                        outFile.write(ns)
                        outFile.write(line)
                        # we turn on the flag to indicate that we want that page
                        flag = True
                    count+=1
            # we write the content we want to extract
            elif flag:
                outFile.write(line)
                # we turn off the flag if we have reached the end of the page
                if line.lstrip()[:7] == "</page>":
                    flag=False
                    # we can even break the loop, as we are extracting only one page
                    break
            else:
                continue



"""
Main part of the program.

Iterates over the list of pages.
For each page, finds the correct archive, unzips it, and extracts data for that page.
"""

progress_message(f"Starting. Number of pages to process: {len(pages)}")

for current_page in pages:
        progress_message(f"Processing page ID {current_page}")
        
        # first, we find which file contains the page we want
        current_file = find_file(current_page)
        progress_message(f"Extracting file {current_file}")
        subprocess.call(["7za","-y","e",current_file,"-o"+folder_out])
        
        # the resulting file has the same name, without the .7z extension
        # next, we extract just the content for that page
        progress_message(f"Extracting XML content for the page")
        unzipped_file = folder_out+current_file[len(folder_in):-3]
        extract_XML(current_page,unzipped_file,folder_out)

        # finally, we delete the initial XML as we are no longer using it
        progress_message(f"Deleting file {unzipped_file}")
        subprocess.call(["rm",unzipped_file])

progress_message("Done.")
