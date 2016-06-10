#REQUIRES BIOPYTHON TO BE INSTALLED
#REQUIRES NCBI+ TO BE INSTALLED
#REQUIRES DANTE MODULE


from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline

import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors

try:
    dante.log("Running BLAST.GetCloseReps.py")

    #Get search information from user
    rep_number = dante.getNumber("How many representatives do you want?")
    dante.log("How many representatives do you want?")
    dante.log(rep_number)
    database = str(raw_input("Which database do you want to search?"))
    dante.log("Which database do you want to search?")
    blast_db_format = 5  #exports hits as XML
    dante.log("Database format")
    dante.log(blast_db_format)

    #allows multiple inputs at command line or will ask for an input file
    #gets a list of fasta files
    for filename in dante.makeFileList(sys.argv):
        dante.log("Input Filename")
        dante.log(filename)
        file_name_xml = dante.makeNewFileName("Desktop/Output", filename, str(".BLAST." + database + ".top" + str(rep_number) + "hits.xml"))
        dante.log("Filename of XML file")
        dante.log(file_name_xml)
        file_name_summary = dante.makeNewFileName("Desktop/Output", file_name_xml,".summary.tsv")
        dante.log("Filename of Summary file")
        dante.log(file_name_summary)
        blastn_cline = NcbiblastnCommandline(remote=True, query=filename, db=database, outfmt=blast_db_format, out= file_name_xml, max_target_seqs =rep_number)

        dante.log(blastn_cline)

        stdout, stderr = blastn_cline()

        dante.BLASTSummary(file_name_xml, file_name_summary)

                        
        print "_____Summary_____"
        print "For filename: ", filename
        print "Output files:"
        print file_name_xml, "\n", file_name_summary
         
except:
    traceback.print_exc(file=sys.stdout)
    dante.log(traceback.format_exc())
    exit(0)
