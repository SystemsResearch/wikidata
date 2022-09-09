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

- You could do the same thing in a shell script, but many of you are probably more comfortable with Python.

- Each XML file is typically over 30GB. 
  
  - Please be mindful about how many unzipped files you keep. If you are working with a large number of files, consider processing them one at a time and deleting them as soon as you have the data you need.
  
  - Your home folder has limited disk space. Make sure to create your own folder in `/work/wikidata/` and to use it as the output folder.



## Submitting jobs

...
