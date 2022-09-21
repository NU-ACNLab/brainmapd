import os
import csv

#initialize directories and files at the global level
directory = "/projects/b1108/data/BrainMAPD"
output = "audit_file_list.csv"
summary_file = "audit_summary.csv"
error_file = "audit_errors.csv"

#initialize a list that keeps track of unique session/scans pairings
ses_scan_list = []

def subj_iterator():
    participants = []
    for subject in os.listdir(directory):
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

        #iterate through sessions and find files
        for session in os.listdir(subj_dir):
            for scan in os.listdir(subj_dir + "/" + session):
                if(not scan[0] == "."):
                    for file in os.listdir(subj_dir + "/" + session + "/" + scan):
                        line = subject + "," + session + "," + scan
                        writer.writerow([line])

                        #check if we seen this scan type before for sessions
                        if(not ses_scan_list.contains([session,])):
                            ses_scan_list.append(session+"_"+scan)


def create_audit_summary(partic):
    with open(summary_file, "a") as sum_file, open(output, "r") as file_list:
        writer = csv.writer(sum_file, delimiter=',')
        reader = csv.reader(file_list, delimiter=",")
        #creates header row from our unique session + scan combo list
        writer.writerow(','.join(str(item) for item in ses_scan_list))
#for each partic, write row to check if they have all sets of files


def main():
    partic_list = subj_iterator()

    #create headers for both files
    with open(output, "w") as audit_file:
        all_files = csv.writer(audit_file, delimiter=',')
        all_files.writerow("subject, session, file")

    for partic in partic_list:
        if(partic[0:3] == "sub"):
            subj_writer(partic)

    with open(summary_file, "w") as sum_file:
        summary = csv.writer(sum_file, delimiter=',')
        summary.writerow(','.join(str(item) for item in ses_scan_list))        
    create_audit_summary(partic)

if __name__ == "__main__":
    main()
