"""filefinder.py: Determines which files exist for each
    participant for brainMAPD data"""

__author__   = "Katharina Seitz"
__date__     = "9/22/22"

import os
import csv

#initialize directories and files at the global level
directory = "/projects/b1108/data/BrainMAPD"
output = "audit_file_list.csv"
summary_file = "audit_summary.csv"
error_file = "audit_errors.csv"

#initialize a list that keeps track of unique session/scans pairings
ses_scan_list = []
#define file dict as well that keeps track of what scan each participant has
partic_scans = {}

'''
    Iterates through the globally defined directory 'directory', 
    and populates a list of all of the participants we have data
    for. 
            Parameters:
                    none
            Returns:
                    a list of participants
'''
def subj_iterator():
    participants = []
    for subject in os.listdir(directory):
        if(subject[0:3] == "sub"):
	        participants.append(subject)
    return participants

'''
    Takes a single participant, and looks through their data folders to 
    populate the output file with all files for that participant. Also 
    populates a list of unique session/scans, and 
            Parameters:
                    a: subject
            Returns:
                    none
'''
def subj_writer(subject):
    #define subject level directory
    subj_dir = directory + "/" + subject

    #open csv
    with open(output, "a") as audit_file:
        writer = csv.writer(audit_file, delimiter=',')
        #list that keeps track of what scan this partic has
        scans = []
        #iterate through sessions and find files
        for session in os.listdir(subj_dir):
            for scan in os.listdir(subj_dir + "/" + session):
                if(not scan[0] == "."): #ignores hidden files
                    for file in os.listdir(subj_dir + "/" + session + "/" + scan):
                        line = subject + "," + session + "," + file
                        writer.writerow([line]) #writes row for each scan file
                        #check if we seen this scan type before for sessions
                        #if not, add to the ses_scan_list to keep track of 
                        #what files a participants could have at most. 
                ses_scan = session + "_" + scan
                if(not ses_scan in ses_scan_list):
                    ses_scan_list.append(ses_scan)
                #adds this scan to this partics list for each scan that we iterate through
                scans.append(ses_scan)
        #this populates the gloabl dict for what scans each particpant has        
        partic_scans[subject] = scans

'''
    Takes a single participant and looks through the partic_scan global dict.
    Based on which scans the partic has, assigns binary value which creates a row
    in the audit_summary.csv file. 
            Parameters:
                    a: subject
            Returns:
                    none
'''
def create_audit_summary(partic):
    #open summary_file (global) in append mode
    with open(summary_file, "a") as sum_file:
        writer = csv.writer(sum_file)
        this_partic_scans = partic_scans[partic] #looking only at this subject
        line = []
        for ses_scan in ses_scan_list: #looks at total list of possible scans
            if ses_scan in this_partic_scans: #determines if this partic has scan
                line.append("1") #assigs 1 or 0 accordingly
            else:
                line.append("0")
        complete_line = partic + "," + ','.join(str(item) for item in line) #makes list to string
        writer.writerow([complete_line])  #writes above string to file

def main():
    partic_list = subj_iterator()

    #create header for the list of files file.
    with open(output, "w") as audit_file:
        all_files = csv.writer(audit_file, delimiter=',')
        all_files.writerow("subject, session, file")

    #calls subj_writer for each partic
    for partic in partic_list:
        subj_writer(partic)

    #writes header for audit summary file
    with open(summary_file, "w") as sum_file:
        summary = csv.writer(sum_file)
        header = "subject_id"
        for item in ses_scan_list:
            header = header + "," + item
        summary.writerow([header]) 

    #calls the function which adds a line for each participant
    #to the audit summary file
    for partic in partic_list:          
        create_audit_summary(partic)

if __name__ == "__main__":
    main()
