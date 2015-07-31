import os
import re


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
    
