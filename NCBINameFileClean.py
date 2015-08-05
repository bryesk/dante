#NCBI NAME CLEAN UP#
#GOAL: To remove extra NCBI header information to see only species names
#Workflow: takes a dante names file and removes any NCBI leading ID numbers if present

import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors
import re             #regular expressions

try:
    #If filenames were passed at the command line, runs getReps on every file. Else, asks for files for input
    for file_name in dante.makeFileList(sys.argv):
        file_name_new = dante.makeNewFileName ("Desktop/Output", file_name, ".cleaned.names")
        with open(file_name,'r') as f, open(file_name_new,'w') as g:
            dante.printOutput(file_name_new)
            line_is_one = True  #allows for alternating lines
            for line in f:
                if line_is_one:
                   line_is_one = False
                   g.write(line)
                else:
                    line_is_one = True
                    #regex matches beginning of NCBI header
                    searchObject=re.search(r'^[a-z]*\|[0-9]*\|[a-z]*\|[0-9a-zA-Z\._]*\|[\s^\n]*', line)
                    if searchObject == None:
                        g.write(line)  #writes original line if no regex match
                    else:
                        g.write(line.replace(searchObject.group(),""))  #writes end of line if regex match
                        
except:
    traceback.print_exc(file=sys.stdout)
    exit(0)


#test
#python Dropbox/dante/NCBINameFileClean.py Dropbox/Bioinformatics/Sequences/ssuAlign/MFBacFrontAlign1/MFBacFrontAlign1.bacteria.mask.afa.names
