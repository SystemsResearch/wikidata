# Wikidata resources

Code to work with Wikipedia dump data.

This is primarily targeted at students enrolled in [IFN703](https://www.qut.edu.au/study/unit?unitCode=IFN703) and [IFN704](https://www.qut.edu.au/study/unit?unitCode=IFN704), the Advanced Project units in the [Master of Data Analytics](https://www.qut.edu.au/courses/master-of-data-analytics) at QUT.

The explanations below (especially those on computational resources) may not completely make sense if you are not a current student.

## Example files

A number of examples are provided here. For each of them, the aim is simplicity rather than convenience. Feel free to modify them to suit your own needs.

Note that, as part of aiming for simplicity, a number of important values (page IDs, input / output folders, etc.) are hard-coded rather than passed as parameters. Make sure to update them as needed for your own work.

### Unzipping

The data is available as a collection of 7zip archive files, each corresponding to a single XML file. Processing you can extract data from the XML files, you need to unzip the archives.

File `unzip.py` is a simple example of how you can automate this. It iterates over a list of 7zip files. For each file, it unzips it to the specified folder.

Quick notes:

- This takes about 2-3 minutes per file.

- You could do the same thing in a shell script, but many of you are probably more comfortable with Python.

- Each XML file is typically over 30GB. 
  
  - Please be mindful about how many unzipped files you keep. If you are working with a large number of files, consider processing them one at a time and deleting them as soon as you have the data you need.
  
  - Your home folder has limited disk space. Make sure to create your own folder in `/work/wikidata/` and to use it as the output folder.

### Extracting specific pages

For your project, you may be working with a selection of some specific pages, rather than the whole collection.

File `unzip_and_extract_based_on_IDs.py`  is an example of how to do this. For each page in a list of IDs, it identifies which archive contains this page (using the fact that each filename contains the IDs of the first and last page of the range contained in the file), and then extracts from that XML only the content for the page of interest and saves it to a new XML file.

Quick notes:

- This should take roughly 3-10 minutes per page (based on limited testing), depending on where the page is located in the file.

- To find the ID for a given page, an easy solution is to use the Wikipedia API.

- You can do this manually:
  
  - Imagine you want to the ID for the Wikipedia page on QUT, for which the URL is https://en.wikipedia.org/wiki/Queensland_University_of_Technology
  
  - The page title is `Queensland_University_of_Technology`
  
  - You can use this title as a query, using this link: https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles=Queensland_University_of_Technology&format=json
  
  - This will return:
    
    ```
    {"batchcomplete":"","query":{"normalized":[{"from":"Queensland_University_of_Technology","to":"Queensland University of Technology"}],"pages":{"198332":{"pageid":198332,"ns":0,"title":"Queensland University of Technology","pageprops":{"defaultsort":"Queensland University of Technology","wikibase-shortdesc":"University in Australia","wikibase_item":"Q1144750"}}}}}
    ```
  
  - From this, you know that the page ID is 198332.

- If you want to do this for a lot of them, you may want to automate these steps.

### Extracting everything but the text

A number of you are working on questions around temporal dynamics (when edits are made, how frequently pages are updated, etc.) or user behaviour (who contributes to which pages, etc.). 

This type of questions does not require the text of each page you analyse. However, that text takes most of the disk space used by the XML files, as you have the complete text for every revision of every page.

You will need to extract just the features that are relevant to your research questions.

File `unzip_and_extract_all_but_text.py` is an example where we iterate over a list of files, unzip them, and extract everything but the text. For the first file in the data dump, the resulting file is 223MB, compared to 35GB if we keep the text.

It means you can then use tools such as `ElementTree` or `BeautifulSoup` to parse the data (which would not be practical with the intial files).

Quick notes:

- This should take about 3-10 minutes per file (based on limited testing).
  
  - Files with higher page IDs contain pages with fewer revisions (as the pages are more recent), which are each processed faster, but they also contain more pages.

- Do not run this on the entire collection unless you want to work with all pages.

- You can combine this example with parts of the previous one, if you want to extract the data for specific pages rather than whole files.

### Extracting from XML to CSV

Even after removing the text as described above, the files still cannot be analysed as in, and still contain a lot of unnecessary elements. For your analysis, you will only need the values (e.g., usernames, timestamps), not the file structure.

File `xml_process_example.py` is an example of how to extract that information, by parsing the XML files using `Beautiful Soup`.

Quick notes:

- In my limited tests, it took 15 minutes to process two files.

- If you are running on HPC, make sure your submission is loaded the appropriate modules for `lxml` and `BeautifulSoup`. Please look at `xml_process.sh` for an example of how to do that.

- As before, you can combine this example with some strategies discussed earlier, for instance of you only want to extract data for some pages.

## Submitting jobs

All your data extraction needs to be submitted as HPC jobs using `qsub`. You **should not** run your programs directly from the command line.

File `example_job.sh` gives you the basic structure of a submission script. It shows you how to specify which resources you need, how to receive notifications about your submitted job, and how to list the commands you want to run.

As per the PDF guide shared on Slack, you submit this script by typing `qsub example_job.sh`. This will return your job details, such as `2857930.pbs`. You can use these details to check the status of your job, by typing `qstat 2857930`.

Quick notes:

- Make sure to change the email address for the notifications. I do not need to know about your jobs...

- Think before asking for resources:
  
  - It is not good to underestimate them
    
    - If your job needs much longer than the specified walltime, it will be killed by the scheduler.
    
    - If you do not have enough memory for your tasks, performance will be low.
  
  - It is not good to overestimate either
    
    - If you ask for a lot of resources, you will wait longer in the queue.
