#FASTA to PHYLIP + NAMES
#This program simplifies names to 10 characters and creates a cross reference file.
#It then returns a PHYLIP sequential formatted sequence file.  
#This program allows multiple file names to be called as arguments.

#Last updated: 2015.8.12

import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors

try:
    
    for file_name in dante.makeFileList(sys.argv):
        file_clean = dante.fastaClean(file_name)
        file_name_phylip = dante.makeNewFileName ("Desktop/Output", file_clean, ".phylips")
        file_name_names = dante.makeNewFileName ("Desktop/Output", file_clean, ".dnames")


        with open(file_clean,'r') as f: 
            
            #NEED TO GO THROUGH ALL THE LINES OF THE REFERENCE FILE AND WRITE THE HEADER LINE TO A NEW LIST
            
            #create phylip header (count number of sequences and the number of characters in first sequence)
            sequence_number = 0
            character_number = 0
            
            for line in f:
                if line [0] == ">":
                    sequence_number = sequence_number + 1
                else:
                    if sequence_number == 1:
                        character_number = character_number + len(''.join(line.split()))

            
        with open(file_clean,'r') as f, open(file_name_phylip, 'w') as g, open(file_name_names,'w') as h:
            #Write phylip header (contains number of sequences and the number of characters in each sequence
            g.write(str(sequence_number) + " " + str(character_number))
            #initial sequence name
            new_name = 'SEQ0000000'
            names_number = 0
            
            for line in f:
                if line[0] == ">":
                    #write new name to name file and phylip document                    
                    h.write(new_name + "\n")
                    g.write("\n" + new_name + " ")
                    
                    #write this line to name file (minus >)
                    h.write(line.strip('>'))

                    #set up next name
                    names_number = names_number + 1
                    new_name = new_name[:-len(str(int(names_number)))] + str(names_number)
                    
                else:
                    g.write(''.join(line.split()))

           
        dante.log ("Program ran: FASTAtoPHYLIPandNAMES.py")
        dante.log ("Input file: " + file_name)
        dante.log ("Output file 1: " + file_name_phylip)
        dante.log ("Output file 2: " + file_name_names)
        
except:
    traceback.print_exc(file=sys.stdout)
    exit(0)

#TEST COMMAND
#  python link/dante/FASTAtoPHYLIPandNAMES.py link/dante/testfiles/TestAlign.fasta
