	### This script generates submission scripts for fmriprep for the first visit
### to run for all participants put "sub-*" in the subDirs variable definition
###
### Anna Cichocki, Ann Carroll
### December 20, 2021
### make sure you add module load numpy to your bash, or run that on the CLI before running this script ('module load numpy')
### make sure to delete any prior output if you intend to rerun the script, otherwise this script will not run (i.e. so that data will not be accidentally overwritten)
### to run: python [script name] [Cichocki OR Carroll]

##except for the config file argument, change indir and outdir to hard-coded path in cmd (without "/" at the end following the .simg argument)

import os
import shutil
import re
import numpy
import glob
import sys

indir = '/projects/b1108/data/BrainMAPD/'
outdir = '/projects/b1108/studies/brainmapd/data/processed/neuroimaging/mid/'
launchdir = '/projects/b1108/studies/brainmapd/scripts/process/mid_fmriprep/launch_test/'
scriptsdir = '/projects/b1108/studies/brainmapd/scripts/process/mid_fmriprep/'
sbatch_name = sys.argv[1]	##EDIT EACH TIME with  your last name to call on a different batch script for submitting jobs

subDirs = glob.glob(indir + "sub-10161")

for subDir in subDirs:
#we changed index 6 to 5 based on BrainMAD folder structure:
    subj = subDir.split('/')[5]
    if not os.path.exists(outdir+subj):
        os.mkdir(outdir+subj)
    unprocessed_sessions = numpy.setdiff1d(os.listdir(indir+subj), os.listdir(outdir+subj))
    for ses in unprocessed_sessions:
        if not os.path.exists(outdir+subj+'/'+ses):
            os.mkdir(outdir+subj+'/'+ses)
# ellyn got rid of the "sub-"       participant_label = subj.split('-')[1]
# we copied then removed        participant_label = subj
# we removed 'SINGULARITYENV_TEMPLATEFLOW_HOME='+outdir+'.cache/templateflow' from the first argument of cmd below:
        cmd = ['singularity', 'run', '--cleanenv', '-B /projects/b1108:/projects/b1108', '/projects/b1108/software/singularity_images/fmriprep-20.2.3.simg', '/projects/b1108/data/BrainMAPD', '/projects/b1108/studies/brainmapd/data/processed/neuroimaging/mid', 'participant', '--participant-label', subj, '--fs-license-file /projects/b1108/software/freesurfer_license/license.txt', '--fs-no-reconall', '-w /projects/b1108/studies/brainmapd/data/processed/neuroimaging/mid/work', '--output-spaces MNI152NLin6Asym', '--skull-strip-template OASIS30ANTs', '--bids-filter-file', scriptsdir+'config/'+ses+'_config.json', '--skip_bids_validation']
        fmriprep_script = launchdir+subj+'_'+ses+'_fmriprep_run.sh'
        os.system('cat '+scriptsdir+'sbatchinfo_'+sbatch_name+'.sh > '+fmriprep_script)
        os.system('echo '+' '.join(cmd)+' >> '+fmriprep_script)
        os.system('chmod +x '+fmriprep_script)
#        os.system('sbatch -o '+launchdir+subj+'_'+ses+'.txt'+' '+fmriprep_script)
