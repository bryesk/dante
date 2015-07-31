#goes through FASTA file- gets a representative sequence from each genus
#this is not random, and will pick the first member it sees
#can take multiple file names as an argument at the command line


#imports os to create file directories
import os
#imports sys to help with file input
import sys
#import regular expression
import re
#import traceback to help with exceptions
import traceback
#import dante functions
import dante

try: 

    def getReps(file_name_fun):
        
        with open(file_name_fun,'r') as f:
            #creates new file name for representative sequences, creates, and opens the file
            file_name_new = dante.makeNewFileName ("Desktop/Output", file_name_fun, ".reps.fasta")
            newFile = open(file_name_new,'w')
            print "\n"
            print 'Input File:  %s' % (file_name_fun)
            print 'Output File: %s' % (file_name_new) 

            #goes through each line in f
            printsequences = False
            genusList = []
            
            for line in f:
                #print line #used for testing
                #if the line is a new header line, test to see if the genus had been seen before
                if line[0] == ">":
                    searchObject=re.search(r'\|\s\w*\s', line) #this matches "| genusname " in NCBI FASTA files
                    if searchObject == None:  #if re.search finds nothing, it returns None.
                        printsequences = False  #if it can't find a genus name, it does not print the sequences
                    else:
                        genusName = searchObject.group()
                        #test to see if the genus has already been seen
                        if genusName not in genusList:
                            genusList.append(genusName)
                            printsequences= True
                            newFile.write(line)
                        else:
                            printsequences = False
                    
                #if the line is a not the start of a new sequence
                #write the line to the new file if it is a continuation of a previous sequence 
                else:
                    if printsequences == True:
                        newFile.write(line)
            newFile.close()

    #If filenames were passed at the command line, runs getReps on every file

    if len(sys.argv) > 1:  #the first argument in sys.argv is always the script name
        file_names = sys.argv[1:] #removes the script name from the list of files to be tested
        #Runs get reps on each file
        for filename in file_names:
            getReps(filename)
    else:
        file_name = str(raw_input('Enter the file to be sampled: '))
        getReps(file_name)
except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
