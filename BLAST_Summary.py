#REQUIRES BIOPYTHON TO BE INSTALLED
#REQUIRES DANTE MODULE

import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors

try:
    dante.log("Running BLAST_Summary.py")

    #allows multiple inputs at command line or will ask for an input file
    #gets a list of fasta files
    for filename in dante.makeFileList(sys.argv):
        file_name_new = dante.makeNewFileName ("Desktop/Output", filename,".summary.tsv")
        dante.log(str("Original File Name: " + filename))
        dante.log(str("New File Name: " + file_name_new))
        dante.BLASTSummary(filename, file_name_new)
        print "_____Summary_____"
        print "For filename: ", filename
        print "Output file: ", file_name_new 
    
except:
    traceback.print_exc(file=sys.stdout)
    dante.log(traceback.format_exc())
    exit(0)
