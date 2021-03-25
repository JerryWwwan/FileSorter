# FileSorter
Jerry Wan
z84715@gmail.com

Overview
-------------
This is a file sorter. A small tool to help you organize files.  
It can add or delete tags in specific name positions.  
It can put files into folders according to title/tag.  
Or move all files from folder.  
He can count the number of files in the folder and name the folder.  
I hope this tool can help you organize your files more easily!!  

Environment
-------------
 Pyton3.7.2 or higher 
 1. if you want to use File Sorter by terminal, please  
 `$ pip install argprase`  
 and  
 `$ python sorter.py -h`  
 to get the help page
 2. Or you can double click  `Sorter_UI.exe` to execute UI application in Windows OS

Usage
-------------
>File's name rule : (title)_(tag1)#(tag2)-num.any

function:

1. sort: Sort files into directories by specific tag.(title,tag1,tag2)
2. fetch: Fetch files from all directories.
3. add: Add string to all of files in directories. (tag1,tag2)
4. remove: Remove string to all of files in directories.(tag1,tag2)
5. size: Calculate the number of files and name number to folder
