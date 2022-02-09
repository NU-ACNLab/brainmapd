#!/bin/bash
#SBATCH --account=p31553                                   ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=normal                                 ## PARTITION (buyin, short, normal, w10001, etc)
#SBATCH --time=16:00:00                                   ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=30G                                ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name="MID_fmriprep_preproc"   ## use the task id in the name of the job
#SBATCH --output=MID_fmriprep_preproc.%A.out                     ## use the jobid (A)
#SBATCH --mail-type=FAIL                                  ## you can receive e-mail alerts from SLURM when your job begins and when your job finishes (completed, failed, etc)
#SBATCH --mail-user=anncarroll2021@u.northwestern.edu    ## your email

module load singularity/latest

