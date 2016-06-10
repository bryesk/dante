#Replaces placeholder names in a tree file with full names. 
#This program works only on TRE files with a dante formatted names file
#The first argument passed to the program will be the TRE file.
#The second argument passed to the program will be the dante formatted names file.


import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors
import re             #regular expressions

try:

    max_name_length = str(raw_input('What is the maximum name length allowed?:' ))  #sets the maximum length of a name

    #Decide if file names are present as arguments or if the script needs to ask.    
    if len(sys.argv) > 2:  #the first argument in sys.argv is always the script name
        file_names = sys.argv[1:]
        #run the changeToFasta command on every file name if other commands are given
        tre_file = sys.argv[1]
        names_file = sys.argv[2]
    else:
        tre_file = str(raw_input('Enter the tree file to be changed: '))
        names_file = str(raw_input('Enter the names file: '))

    file_name_new = dante.makeNewFileName ("Desktop/Output", tre_file, ".namesfixed.tre")
    dante.printOutput(file_name_new)
    
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
                if len(line.strip()) <= max_name_length:    #truncates names down to 50 characters
                    new_line = line
                else:
                    new_line = line.strip()[:max_name_length -1] #truncates to 50 characters

                #this keeps adding numbers to the end of the line until the line is unique
                x=1
                while new_line in names_dict.values():
                    new_line = new_line [:((len(new_line) - len(str(x))-1))] + str(x)
                    x = x + 1
                    print new_line
                names_dict[current_key] = new_line #Creates a dictionary key/value pair.



    with open (tre_file, 'r') as f, open(file_name_new,'w') as g:
    #creates new file name for the new tre, creates, and opens the file
    #runs through each line in the tre file
        for line in f:
            #for each line, runs through each possible short name.
            modified_line = line
            for i in names_dict:
                #looks for the short name. If found, looks up the long name, removes special characters,
                #then writes it to the modified_line variable
                modified_line = modified_line.replace(i, (re.sub(r'[(),:;]','',names_dict[i])))

            #after all short names have been searched, writes the modified line to the new file
            g.write(modified_line)
except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
