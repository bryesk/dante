#converts FASTQ files from NCBI to FASTA files
#can take a file name or list of file names as an input
#Last updated 2015.8.10

import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors


try: 

    for file_name in dante.makeFileList(sys.argv):
        file_name_new = dante.makeNewFileName ("Desktop/Output", file_name, ".fasta")
        dante.printOutput(file_name_new)
        with open(file_name,'r') as f, open (file_name_new, 'w') as g:

            #goes through each line in f
            trigger = False
            for line in f:
                print line
                if line.isspace() == False:
                    #write the next line if a header line occured previously   
                    if trigger:
                        newFile.write(line)
                    #if "@" header line, write to file
                    if line[0] == "@":
                        #change header information to fasta format
                        #(send everything but the @ sign to spaceToBar
                        g.write(">" +line[1:])
                        #set up so that the next line will automatically be written
                        trigger = True
                    #do not write next line if not "@" header
                    #skip "+" header lines and quality data
                    else:
                        trigger = False

except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
