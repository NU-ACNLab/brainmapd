"""filefinder.py: Determines which files exist for each
    participant for brainMAPD data"""

__author__   = "Katharina Seitz"
__date__     = "9/22/22"

import os
import csv
import glob

#initialize directories and files at the global level
directory = "/projects/b1108/data/BrainMAPD"
output = "audit_file_list.csv"
summary_file = "audit_summary_count.csv"
error_file = "audit_errors_count.csv"
file_checker = "subj_file_check.csv"


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
    with open(output, "a") as audit_file, open(file_checker, "a") as file2:
        writer = csv.writer(audit_file, delimiter=',')
        writer2 = csv.writer(file2, delimiter=',')
        #list that keeps track of what scan this partic has
        scans = []
        #iterate through sessions and find files
        for session in os.listdir(subj_dir):
            for scan in os.listdir(subj_dir + "/" + session):
                if(not scan[0] == "."): #ignores hidden files
                    #initializes file count var to make sure we have a complete
                    #set of files for each partcip
                    file_count = 0
                    path = directory + "/" + subject + "/" + session + "/" + scan + "/"
                    #session 1
                    fear_j = len(glob.glob(path + "*FEAR*.json"))
                    fear_n = len(glob.glob(path + "*FEAR*.nii.gz"))
                    mid_j = len(glob.glob(path + "*MID*.json"))
                    mid_n = len(glob.glob(path + "*MID*.nii.gz"))
                    rest_j = len(glob.glob(path + "*REST*.json"))
                    rest_n = len(glob.glob(path + "*REST*.nii.gz"))

                    #session 1
                    if(session == "ses-1" and scan == "anat" and bool(glob.glob(path + "*.json")) and \
                        bool(glob.glob(path + "*.nii.gz"))):
                            writer2.writerow([subject, session, scan, "1"])
                    
                    elif(session == "ses-1" and scan == "func" and \
                        fear_j > 1 and fear_n > 1):
                            writer2.writerow([subject, session, scan, "1"])
                    #session 2
                    elif(session == "ses-2" and scan == "anat" and bool(glob.glob(path + "*.json")) and \
                        bool(glob.glob(path + "*.nii.gz"))):
                            writer2.writerow([subject, session, scan, "1"])

                    elif(session == "ses-2" and scan == "func" and \
                        fear_j > 0  and fear_n > 0 and mid_j > 1 and mid_n > 1 and rest_j > 0 and rest_n > 0):
                            writer2.writerow([subject, session, scan, "1"])
                    #session 3
                    elif(session == "ses-3" and scan == "anat" and bool(glob.glob(path + "*.json")) and \
                        bool(glob.glob(path + "*.nii.gz"))):
                            writer2.writerow([subject, session, scan, "1"])

                    elif(session == "ses-3" and scan == "func" and \
                        fear_j > 1 and fear_n > 1):
                            writer2.writerow([subject, session, scan, "1"])
                    #session 4
                    elif(session == "ses-4" and scan == "anat" and bool(glob.glob(path + "*.json")) and \
                        bool(glob.glob(path + "*.nii.gz"))):
                            writer2.writerow([subject, session, scan, "1"])

                    elif(session == "ses-4" and scan == "func" and \
                        fear_j > 0  and fear_n > 0 and mid_j > 1 and mid_n > 1 and rest_j > 0 and rest_n > 0):
                            writer2.writerow([subject, session, scan, "1"])
                    else: 
                            writer2.writerow([subject, session, scan, "0"])

                    for file in os.listdir(subj_dir + "/" + session + "/" + scan):
                        line = subject + "," + session + "," + file
                        writer.writerow([line]) #writes row for each scan file
                        file_count = file_count + 1 #increment counter 
                        #check if we seen this scan type before for sessions
                        #if not, add to the ses_scan_list to keep track of 
                        #what files a participants could have at most. 
                ses_scan = session + "_" + scan
                if(not ses_scan in ses_scan_list):
                    ses_scan_list.append(ses_scan)
                #adds this scan to this partics list for each scan that we iterate through
                scans.append([ses_scan, file_count])
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
        scans = []
        counts = []
        for scan_count in this_partic_scans:
            scans.append(scan_count[0])
            counts.append(scan_count[1])
        line = []
        for ses_scan in ses_scan_list: #looks at total list of possible scans
            found_scan = 0
            counter = 0
            for scan in scans:
                if scan == ses_scan:
                    line.append(counts[counter])
                    found_scan = 1
                counter = counter + 1
            if found_scan == 0:
                line.append(0)
        complete_line = partic + "," + ','.join(str(item) for item in line) #makes list to string
        writer.writerow([complete_line])  #writes above string to file

def main():
    partic_list = subj_iterator()

    with open(file_checker, "w") as file2:
        writer = csv.writer(file2, delimiter=",")
        writer.writerow("subject, session, scan, yes_no")

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
