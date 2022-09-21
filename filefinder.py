import os
import csv

#initialize directories and files at the global level
directory = "/projects/b1108/data/BrainMAPD"
output = "audit_file_list.csv"
summary_file = "audit_summary.csv"
error_file = "audit_errors.csv"

#initialize a list that keeps track of unique session/scans pairings
ses_scan_list = []
#define file dict as well
partic_scans = {}

def subj_iterator():
    participants = []
    for subject in os.listdir(directory):
        if(subject[0:3] == "sub"):
	        participants.append(subject)
    return participants


'''
    Copies a single particpant's bids files from old Georgia directories to new 
    /studies/foundations data format. Behavioural data goes into behavioral folder, rather than
    bids
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
        scans = []
        #iterate through sessions and find files
        for session in os.listdir(subj_dir):
            for scan in os.listdir(subj_dir + "/" + session):
                if(not scan[0] == "."):
                    for file in os.listdir(subj_dir + "/" + session + "/" + scan):
                        line = subject + "," + session + "," + file
                        writer.writerow([line])
                    

                        #check if we seen this scan type before for sessions
                        #if not, add to the ses_scan_list to keep track of 
                        #what files a participants could have at most. 
                ses_scan = session + "_" + scan
                if(not ses_scan in ses_scan_list):
                    ses_scan_list.append(ses_scan)
                scans.append(ses_scan)
        partic_scans[subject] = scans


def create_audit_summary(partic):
    with open(summary_file, "a") as sum_file:
        writer = csv.writer(sum_file)
        this_partic_scans = partic_scans[partic]
        line = []
        for ses_scan in ses_scan_list:
            if ses_scan in this_partic_scans:
                line.append("1")
            else:
                line.append("0")
        complete_line = partic + "," + ''.join(str(item) for item in line)
        writer.writerow(complete_line) 



def main():
    partic_list = subj_iterator()

    #create headers for both files
    with open(output, "w") as audit_file:
        all_files = csv.writer(audit_file, delimiter=',')
        all_files.writerow("subject, session, file")

    for partic in partic_list:
        subj_writer(partic)

    with open(summary_file, "w") as sum_file:
        summary = csv.writer(sum_file)
        summary.writerow(','.join(str(item) for item in ses_scan_list)) 

    for partic in partic_list:          
        create_audit_summary(partic)

if __name__ == "__main__":
    main()
