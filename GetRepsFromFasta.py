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

try: 

    #Function for removing the directory of a file name
    def getFilename(whole_name):
        reversed_name = whole_name[::-1]
        trun_rev=""
        for i in range(len(whole_name)):
            if reversed_name[i] == "/":
                break
            else:
                trun_rev = trun_rev + reversed_name[i]
        new_name = trun_rev[::-1]
        return (new_name)

    def getReps(file_name_fun):
        
        with open(file_name_fun,'r') as f:
            #creates new file name for representative sequences, creates, and opens the file
            file_name_new = getFilename(file_name_fun)
            file_name_new = directory+"/"+file_name_new+ ".rep.fasta"
            newFile = open(file_name_new,'w')

            #goes through each line in f
            printsequences = False
            genusList = []
            
            for line in f:
                #print line #used for testing
                #if the line is a new header line, test to see if the genus had been seen before
                if line[0] == ">":
                    searchObject=re.search(r'\|\s\w*\s', line) #this matches "| genusname " in NCBI FASTA files
                    genusName = searchObject.group()
                    #print genusName #used for testing
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

    
    #creates the "Output" file on the Desktop if it does not already exist.
    directory = "Desktop/Output"
    if not os.path.exists(directory):
        os.makedirs(directory)

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
