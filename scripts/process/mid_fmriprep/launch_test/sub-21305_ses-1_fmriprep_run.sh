#!/bin/bash
#SBATCH --account=p30971                                   ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=normal                                 ## PARTITION (buyin, short, normal, w10001, etc)
	##SBATCH --array=1                                         ## number of jobs to run "in parallel"
	##SBATCH --nodes=1                                         ## how many computers do you need
	##SBATCH --ntasks-per-node=1                               ## how many cpus or processors do you need on each computer
#SBATCH --time=16:00:00                                   ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=30G                                ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name="MID_fmriprep_preproc"   ## use the task id in the name of the job
#SBATCH --output=MID_fmriprep_preproc.%A.out                     ## use the jobid (id)
#SBATCH --mail-type=FAIL                                  ## you can receive e-mail alerts from SLURM when your job begins and when your job finishes (completed, failed, etc)
#SBATCH --mail-user=annacichocki2025@u.northwestern.edu    ## your email

module load singularity/latest

singularity run --cleanenv -B /projects/b1108:/projects/b1108 /projects/b1108/software/singularity_images/fmriprep-20.2.3.simg /projects/b1108/data/BrainMAPD /projects/b1108/studies/brainmapd/data/processed/neuroimaging/mid participant --participant-label sub-21305 --fs-license-file /projects/b1108/software/freesurfer_license/license.txt --fs-no-reconall -w /projects/b1108/studies/brainmapd/data/processed/neuroimaging/mid/work --output-spaces MNI152NLin6Asym --skull-strip-template OASIS30ANTs --bids-filter-file /projects/b1108/studies/brainmapd/scripts/process/mid_fmriprep/config/ses-1_config.json --skip_bids_validation
