import os
import re
import time
import sys


###MAKE NEW FILE NAME ###
#Takes an directory path, an input file, and a new extention and makes a new file. 
def makeNewFileName (directory, input_file, ext):
    d = os.path.normcase(directory)
    if not os.path.exists(d):
        os.makedirs(d)
    file_name = os.path.splitext(os.path.basename(input_file))[0] + ext
    return os.path.join(os.path.normpath(directory), file_name)


###RUN MULTIPLE FILES###
#Takes a list of file names generated at the command line and generates a list of files to be tested.
#If there are not commands, asks for a file name. 

def makeFileList (file_list_input):
    if len(file_list_input) > 1:  #the first argument in sys.argv is always the script name
        file_names = file_list_input[1:] #removes the script name from the list of files to be tested
        return file_names
    else:
        file_names.append(str(raw_input('Enter the input file path: ')))

###GET E-MAIL###
def getEmail ():
    flag = False
    while not flag:
        email = str(raw_input('Enter e-mail: '))
        flag = re.match(r'[^@]+@[^@]+\.[^@]+',email.strip())
        if not flag:
            print "E-mail does not seem vaild."
    return email.strip()

###PRINT OUTPUT###
def printOutput(file_name_print):
    print "\n"
    print ("Output File Name: %s") %(file_name_print)

###FASTA CLEAN###
def fastaClean(file_name):
    flag = True
    with open(file_name,'r') as f:
        for line in f:
            if "\r" in line:
                flag = False
    if flag:
        return (file_name)
    else:
        file_name_new= makeNewFileName('Desktop/Output', file_name, '.no_cr.fasta')
        with open(file_name, 'r') as f, open(file_name_new, 'w') as g:
            for line in f:
                g.write(line.replace('\r','\n'))
        return (file_name_new)

###LOGGING SYSTEM###

def log (comment):
    if not isinstance(comment,basestring):
        comment = str(comment)
    log_file = os.path.dirname(os.path.realpath(sys.argv[0])) + "/dante.log"
    with open (log_file, 'a') as f:
        print_comment = time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + ": " + comment + "\n"
        f.write(print_comment)
    
#Get a number.###
def getNumber(s):
    while (True):
        number = str(raw_input(s)).strip()
        try:
            float(number)
            return number
        except ValueError:
            None

#READ A FASTA FILE#
def readFASTA (FASTAfile):
    from Bio import SeqIO

    seq_list = []
    
    for seq_record in SeqIO.parse(FASTAfile, "fasta"):
        seq_list.append(seq_record.id,seq_record.seq)
    return seq_list
    
def BLASTSummary(XMLfile, SummaryFile):
    from Bio.Blast import NCBIXML
    with open(XMLfile,'r') as result_handle, open (SummaryFile, 'w') as f:
            f.write(str("Original Name"+ "\t"+"ID"+"\t"+ "Name" +"\t"+ "E-value"+"\t"+"Ident" + "\n"))
            for blast_record in NCBIXML.parse(result_handle):
                if len(blast_record.alignments) >0:
                    for alignment in blast_record.alignments:
                        for hsp in alignment.hsps:
                            f.write(str(blast_record.query) + "\t"+ alignment.hit_id+"\t"+alignment.hit_def+"\t"+ str(hsp.expect) +"\t"+ '{0:.2f}'.format(float(hsp.positives)/hsp.align_length) + "\n")
                else:
                    f.write(str(blast_record.query) + "\t" + "ERROR" + '\n')
