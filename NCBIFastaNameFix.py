#REESTORES FULL LENGTH NAMES FOR NCBI FORMATTED HEADERS 
#This program works only on FASTA files with NCBI formatted headers
#Certain programs will truncate long headers on fasta files. This will restore the name as long as the id number at the start of the header remains, and if the headers are in NCBI format. 

#imports os to create file directories
import os
#imports sys to help with file input
import sys
#import traceback to help with errors
import traceback
import dante

try: 

    if len(sys.argv) >1:
        first_file_name = sys.argv[1]
        second_file_name = sys.argv[2]
    else:
        first_file_name = str(raw_input('Enter the file to be changed: '))
        second_file_name = str(raw_input('Enter the reference file that contains the correct header names: '))

    
    
    #NEED TO GO THROUGH ALL THE LINES OF THE REFERENCE FILE AND WRITE THE HEADER LINE TO A NEW LIST
    headerDict = {}
    with open (first_file_name, 'r') as f:
        for line in f:
            if line[0] == ">":
                headerDict[line.split('|')[1]] = line

    #open file using user supplied name
    new_file = dante.makeNewFileName ('Desktop/Output', second_file_name, ".namesfixed.fasta")
    with open(second_file_name,'r') as f, open(new_file,'w') as g:
        print "\n"
        print ("Output File Name: %s") %(new_file)
        print "\n"
        for line in f:
            #if the line is a new header line, write instead the top of the list
            flag = True
            if line[0] == ">":  #Header lines in fasta format all start with '>'
                test_id = line.split('|')[1] #This only works on NCBI formatted files
                for key in headerDict:
                    if str(test_id) == str(key):  #tests id against key
                        g.write(headerDict[key])
                        flag = False
                if flag:
                    g.write(line)
            else:
                g.write(line)

except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
