import os
import csv

directory = "/projects/b1108/data/BrainMAPD"
output = "audit.csv"

def subj_iterator():
	#intiliaze list of participants 
	participants = []
	#iterates through subject folders to grab the particpants
	for subject in os.listdir(directory):
		#make directory in dest_dir for the new subject
		participants.append(subject)
	return(participants)


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
    with open(output, "w") as audit_file:
        writer = csv.writer(audit_file, delimiter=',')

    #intialize unique list to keep track of session/files
    ses_files_list = []

    #iterate through sessions and find files
    for session in os.listdir(subj_dir):
        for type in os.listdir(subj_dir + "/" + session):
            for file in os.listdir(subj_dir + "/" + session+ "/" + type):
                line = subject + "," + session + "," + file
                writer.writerow(line)
                ses_files_list.append([session, type])
    return ses_files_list
        




def main():
    partic_list = subj_iterator()

    with open(output, "w") as audit_file:
        writer = csv.writer(audit_file, delimiter=',')
        #write header
        writer.writerow("subject, session, file")

    for partic in partic_list:
        subj_writer(partic)
    


if __name__ == "__main__":
    main()
