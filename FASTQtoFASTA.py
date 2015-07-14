#converts FASTQ files from NCBI to FASTA files
#can take a file name or list of file names as an input

#imports os to create file directories
import os
#imports sys to help with file input
import sys
#import traceback to help with errors
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

    def spaceToBar (a_string):
        return_string = ""
        for i in range (len(a_string)):
            if a_string[i] == " ":
                return_string = return_string + "|"
            else:
                return_string = return_string + a_string[i]
        return return_string

    def changeToFASTA(file_name_fun):
        with open(file_name_fun,'r') as f:

            #creates new file name for header information, creates, and opens the file
            file_name_new = getFilename(file_name_fun)
            file_name_new = directory+"/"+file_name_new[:-6]+ ".fasta"
            newFile = open(file_name_new,'w')

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
                        #spaceToBar will turn all " " into "|"
                        newFile.write(">" + spaceToBar(line[1:]))
                        #set up so that the next line will automatically be written
                        trigger = True
                    #skip "+" header lines
                    #do not write next line if not "@" header
                    else:
                        trigger = False

        newFile.close()

    #creates the "Output" file on the desktop if it does not already exist
    directory = "Desktop/Output"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if len(sys.argv) > 1:  #the first argument in sys.argv is always the script name
        file_names = sys.argv[1:]
        #run the changeToFasta command on every file name if other commands are given
        for filename in sys.stdin:
            changeToFASTA(filename)
    else:
        file_name = str(raw_input('Enter the file to be changed: '))
        changeToFASTA(file_name)

except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
