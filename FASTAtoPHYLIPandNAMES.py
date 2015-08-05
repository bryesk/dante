#FASTA to PHYLIP + NAMES
#This program simplifies names to 10 characters and creates a cross reference file.
#It then returns a PHYLIP sequential formatted sequence file.  
#This program allows multiple file names to be called as arguments.

#imports os to create file directories
import os
#imports sys to help with file input
import sys


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

#takes a string and fills up the front until it is 7 characters long. Then appends 'SEQ' to the front. 
def makeTen(num_string):
    num_list = list(num_string)
    while len(num_list) < 7:
      num_list.insert(0,'0')
    return('SEQ' + "".join(num_list))  
        
def createNames(refFile):

    #NEED TO GO THROUGH ALL THE LINES OF THE REFERENCE FILE AND WRITE THE HEADER LINE TO A NEW LIST
    with open (refFile, 'r') as f:
            
        #opens a new file name for names
        file_name_names = getFilename(refFile)
        file_name_names = directory+"/"+file_name_names+ ".dnames"
        namesFile = open(file_name_names,'w')
            
        
        #open a new file to hold phylip document
        file_name_phylip = getFilename(refFile)
        file_name_phylip = directory+"/"+file_name_phylip+ ".phylips"
        phylipFile = open(file_name_phylip,'w')

        names_number = 0

        #create phylip header (count number of sequences and the number of characters in first sequence)
        sequence_number = 0
        character_number = 0
        first_line_trigger = True
        second_line_trigger = True
        for line in f:
            if line [0] == ">":
                sequence_number = sequence_number + 1
            else:
                if sequence_number == 1:
                    character_number = character_number + len(''.join(line.split()))

        phylipFile.write(str(sequence_number) + " " + str(character_number))

    with open (refFile, 'r') as f: 
        for line in f:
            if line[0] == ">":
                #write new name to name file and phylip document
                new_name = makeTen(str(int(names_number)))
                namesFile.write(new_name + "\n")
                phylipFile.write("\n" + new_name + " ")
                names_number = names_number + 1
                #write this line to name file (minus >)
                namesFile.write(line.strip('>'))
            else:
                phylipFile.write(''.join(line.split()))
                

    phylipFile.close()
    namesFile.close()
                
    return()


#creates the "Output" file on the desktop if it does not already exist
directory = "Desktop/Output"
if not os.path.exists(directory):
    os.makedirs(directory)

#MAIN CONTROL BLOCK- ALLOWS FOR CALLING MULTIPLE FILES AS ARGUMENTS
    
if len(sys.argv) > 1:  #the first argument in sys.argv is always the script name
    file_names = sys.argv[1:]
    #run the changeToFasta command on every file name if other commands are given
    for filename in file_names:
        createNames(filename)

else:
    file_name = str(raw_input('Enter the file to be changed: '))
    createNames(file_name)

