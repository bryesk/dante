#REQUIRES BIOPYTHON TO BE INSTALLED
#REQUIRES DANTE MODULE

from Bio.Blast import NCBIXML

import sys            #for helping with command line interface
import dante          #main dante functions
import traceback      #for helping with errors

try:



    #allows multiple inputs at command line or will ask for an input file
    #gets a list of fasta files
    for filename in dante.makeFileList(sys.argv):  
        file_name_new = dante.makeNewFileName ("Desktop/Output", filename,".summary.tsv")
        with open(filename,'r') as result_handle, open (file_name_new, 'w') as f:
            f.write(str("OTU name"+ "\t"+"Closest culture ID"+"\t"+ "Closest Culture Name" +"\t"+ "E-value"+"\t"+"Ident" + "\n"))
            for blast_record in NCBIXML.parse(result_handle):
                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        f.write(str(blast_record.query) + "\t"+ alignment.hit_id+"\t"+alignment.hit_def+"\t"+ str(hsp.expect) +"\t"+ '{0:.2f}'.format(float(hsp.positives)/hsp.align_length) + "\n")

    
except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
