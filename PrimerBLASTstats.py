#PRIMER BLAST STATS
#Asks for text file containing data from PrimerBLAST
#This can be passed as an argument when running from the command line
#Returns a file on the Desktop of the number of on-target sequences, as well as a histogram of PCR bands divided into 100bp widths


#imports os to create file directories
import os
#imports sys to help with file input
import sys
#import traceback to help with Errors
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

    #Function for determining if a string is actually a number.
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    #creates the "Output" file on the desktop if it does not already exist
    directory = "Desktop/Output"
    if not os.path.exists(directory):
        os.makedirs(directory)

    #If an argument is passes, uses it as the file name. Else, asks for a file name. 
    if len(sys.argv) > 1:  #the first argument in sys.argv is always the script name
        print str(len(sys.argv))
        print str(sys.argv[1])
        file_name = sys.argv[1]
    else:
        file_name = str(raw_input('Enter the file to be tested: '))

    #sets up a variable to hold a yes or no response    
    yesno1= "nothing"

    #ALLOWS THE USER TO SPECIFY A DIFFERENT ON-TARGET AREA
    while yesno1 != "Y" and yesno1 != "N":
        yesno1 = str(raw_input('The default base pair range for the on-target region is 1 - 3000. Do you want to enter a different on-target region (Y/N)? :'))
        yesno1 = yesno1[0]
        yesno1 = yesno1.upper()
        if yesno1 != "Y" and yesno1 !="N":
            print "You must enter a Y or N. No other responses are valid\n"

    lower_bp = 1
    upper_bp = 3000
            
    if yesno1 == "Y":
        lower_bp_new= str(raw_input('Please enter lower base pair limit: '))
        upper_bp_new = str(raw_input('Please enter upper base pair limit:'))
        
        if is_number(lower_bp_new):
            lower_bp = float(lower_bp_new)
        else:
            print "You did not enter a number for the lower base pair limit. The default of 1 will be used.\n"
    
        if is_number(upper_bp_new):
            upper_bp = float(upper_bp_new)
        else:
            print "You did not enter a number for the lower base pair limit. The default of 3000 will be used.\n"

    if lower_bp >= upper_bp:
        print "The lower bp number is greater than or equal to your upper bp number. The defaults of 1 for lower and 3000 for upper will be used."
        lower_bp = 1
        upper_bp = 3000

    bp_lengths = []   #for holding the sequence lengths 
    all_sequences = 0 #for counting total number of sequences
        
    #open file using user supplied name
    with open(file_name,'r') as f:

        #goes through each line in f and writes sequence length to bp_lengths
        for line in f:
            if line[0:14] == "product length":
                all_sequences = all_sequences + 1 #counts total number of sequences
                bp_lengths.append(float(line[17:]))

    #set up histogram variables
    lower_hist = 0
    upper_hist = 3000
    width_hist = 100
    counter_hist = lower_hist
    dict_hist = {}
    keys_hist = []
    on_target = 0    
    
    #set up dictionary to hold histogram values (the lower value is the key)
    while counter_hist <= upper_hist:
        dict_hist[counter_hist] = 0
        keys_hist.append(counter_hist)
        counter_hist = counter_hist + width_hist

    counter_hist = lower_hist

    #creates new file name for statistics
    file_name_new = getFilename(file_name)
    file_name_new = directory+"/"+file_name_new+ ".stats.txt"
    newFile = open(file_name_new,'w')
    
    #go through all of the bp lengths found
    for s in bp_lengths:
        #CODE FOR TESTING ON-TARGET BANDS
        if s >=lower_bp and s<=upper_bp:
            on_target = on_target +1
        
        counter_hist = lower_hist #need to initally reset the counter

        #goes through each histogram bin and attempts to put it in one
        while counter_hist < upper_hist:
            if s >= counter_hist and s < (counter_hist + width_hist):
                dict_hist[counter_hist] = dict_hist[counter_hist]+1
                break
            counter_hist = counter_hist + width_hist
        #adds one to the top if above the upper limit
        if s>=upper_hist:
            dict_hist[upper_hist] = dict_hist[upper_hist]+1

    print "Total number of sequences found: " + repr(all_sequences)
    newFile.write("Total number of sequences found: " + repr(all_sequences) + "\n")
    
    print "Number of on-target sequences ("+repr(lower_bp)+ " to " +repr(upper_bp) + " bp) found: " + repr(on_target)
    newFile.write("Number of on-target sequences ("+repr(lower_bp)+ " to " +repr(upper_bp) + " bp) found: " + repr(on_target) + "\n")
    
    print "The histogram values are as follows"
    newFile.write("The histogram values are as follows: \n")
    
    for s in keys_hist:
        if s != keys_hist[-1]:
            print "From " + repr(s) + " to " + repr(s + width_hist) + ' : ' + repr(dict_hist[s])
            newFile.write("From " + repr(s) + " to " + repr(s + width_hist) + ' : ' + repr(dict_hist[s]) + "\n")
        else:
            print "Greater than " + repr(s) + ' : ' + repr(dict_hist[s])
            newFile.write("Greater than " + repr(s) + ' : ' + repr(dict_hist[s]))
    newFile.close()
except:
    traceback.print_exc(file=sys.stdout)
    exit(0)
