#REQUIRES BIOPYTHON TO BE INSTALLED
#REQUIRES DANTE MODULE

#import from Biopython
from Bio.Blast import NCBIXML
from Bio import Entrez
#import traceback to help with exceptions
import traceback
#import dante functions
import dante
#import sys functions
import sys

try:
    #Talking with the NCBI database requires an e-mail address
    print ("NCBI databse requires an e-mail address. ")
    Entrez.email = dante.getEmail()
    #allows multiple inputs at command line or will ask for an input file
    for filename in dante.makeFileList(sys.argv):

        name_set = set()
        name_list=[]
    
        result_handle = open(filename,'r') #open the xml file for reading
        blast_records = NCBIXML.parse(result_handle) #parses the file to a blast_records object
        total = 0
        for record in blast_records: #go through every record generated
            for alignment in record.alignments:
                name_set.add(alignment.title.split('|')[1]) #adds id number to set (removes duplicates)

        with open(dante.makeNewFileName ('Desktop/Output', filename, "seqs.fasta"),'w') as f:
            print ('Output file: %s') %(f)
            for value in name_set: #walks through every id number
                #Biopython for retreving fasta files
                handle = Entrez.efetch(db="nucleotide", id=value, rettype="fasta", retmode="text")
                f.write(handle.read())


except:
    traceback.print_exc(file=sys.stdout)
    exit(0)






