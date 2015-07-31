#Replaces placeholder names in a tree file with full names. 
#This program works only on TRE files with a dante formatted names file
#The first argument passed to the program will be the TRE file.
#The second argument passed to the program will be the dante formatted names file.

#imports os to create file directories
import os
#imports sys to help with file input
import sys
#import regular expression
import re

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

#creates the "Output" file on the desktop if it does not already exist
directory = "Desktop/Output"
if not os.path.exists(directory):
    os.makedirs(directory)

#Decide if file names are present as arguments or if the script needs to ask.    
if len(sys.argv) > 1:  #the first argument in sys.argv is always the script name
    file_names = sys.argv[1:]
    #run the changeToFasta command on every file name if other commands are given
    tre_file = sys.argv[1]
    names_file = sys.argv[2]
else:
    tre_file = str(raw_input('Enter the tree file to be changed: '))
    names_file = str(raw_input('Enter the names file: '))

names_dict ={} #Key = short name. Value = long name.
current_key = ""

#Goes through every line of the names file. 
#Create a list of short names as well as a dictionary using the short name as the key and the full name as the value.
with open (names_file, 'r') as f:
    key_switch = True
    for line in f:
        if key_switch:
            key_switch = False
            current_key = line.strip() #Creates a key to use in a dictionary. Removes newline from key.
        else:
            key_switch = True
            if len(line.strip()) <= 50: 
                names_dict[current_key] = line.strip() #Creates a dictionary key/value pair. Removes newline from value.
            else:
                names_dict[current_key] = line.strip()[:49]

with open (tre_file, 'r') as f:
    #creates new file name for the new tre, creates, and opens the file
    file_name_new = getFilename(tre_file)
    file_name_new = directory+"/"+file_name_new+ ".namesfixed.tre"
    new_file = open(file_name_new,'w')

    #runs through each line in the tre file
    for line in f:
        #for each line, runs through each possible short name.
        modified_line = line
        for i in names_dict:
            #looks for the short name. If found, looks up the long name, removes special characters,
            #then writes it to the modified_line variable
            modified_line = modified_line.replace(i, (re.sub(r'[(),:;]','',names_dict[i])))
        
        #after all short names have been searched, writes the modified line to the new file
        new_file.write(modified_line)
    new_file.close()        
