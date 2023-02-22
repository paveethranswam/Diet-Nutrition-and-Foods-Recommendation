#!/bin/bash
#####  Constructed by HPC everywhere #####
#SBATCH -J seq2rel_job
#SBATCH -A r00082
#SBATCH -p general
#SBATCH -o seq2rel_job.txt
#SBATCH -e seq2rel_job.err
#SBATCH --mail-user=paswam@iu.edu
#SBATCH --nodes 3
#SBATCH --ntasks-per-node 1
#SBATCH --partition=general
#SBATCH --output seq2rel_job_log
#SBATCH --time=04:00:00

######  Module commands #####
module load python
source raPython/bin/activate

######  Job commands go below this line #####
echo '###### Running script ######'
allennlp evaluate "https://github.com/JohnGiorgi/seq2rel/releases/download/pretrained-models/cdr.tar.gz" \
    "custom_main_test_cdr/test_custom.tsv" \
    --output-file "test_metrics_custom.jsonl" \
    --predictions-output-file "test_predictions_custom.jsonl" \
    --include-package "seq2rel"
echo '###### Run Complete! ######'