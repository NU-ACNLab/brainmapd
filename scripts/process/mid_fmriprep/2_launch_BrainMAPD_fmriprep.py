	### This script submits each subj script for a specified session to the cluster
### to run for all participants put "sub-*" in the subDirs variable definition
###
### Anna Cichocki, Ann Carroll
### December 20, 2021
### make sure you add module load numpy to your bash, or run that on the CLI before running this script ('module load numpy')
### make sure to delete any prior output (from launch folder and fmriprep outer folder) if you intend to rerun the script, otherwise this script will not run (i.e. so that data will not be accidentally overwritten)
### to run: python [script name] [session number]

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
ses = sys.argv[1]	##EDIT EACH TIME with  your last name to call on a different batch script for submitting jobs

subjects = ['sub-10029', 'sub-10161']
#sub-10161_"+ses+"_fmriprep_run.sh

subscript = '_ses-'+ses+'_fmriprep_run.sh'
#subscript.split('_')[2]

for subject in subjects:

    if os.path.exists(launchdir+subject+subscript):
         os.system('chmod +x '+launchdir+subject+subscript)
         os.system('sbatch -o '+launchdir+subject+'_ses-'+ses+'.txt '+launchdir+subject+subscript)
    else:
        print("error")
