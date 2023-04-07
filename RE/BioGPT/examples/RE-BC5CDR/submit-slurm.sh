#!/bin/bash
#####  Constructed by HPC everywhere #####
#SBATCH -J biogpt_job_re
#SBATCH -A r00082
#SBATCH -p gpu
#SBATCH -o biogpt_job_re.txt
#SBATCH -e biogpt_job_re.err
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --gpus-per-node v100:1
#SBATCH --mem=100G
#SBATCH --partition=dl
#SBATCH --output biogpt_job_re_log
#SBATCH --time=4:00:00

######  Module commands #####
# module unload python/3.9.8
module load python

#### module load deeplearning - No need to use this as my virtual env has all dl components installed

source /N/u/paswam/Carbonate/raPython/bin/activate

######  Job commands go below this line #####
echo '###### Running script ######'
#python train.py --data_dir docred_data/ --transformer_type roberta --model_name_or_path roberta-base --load_path checkpoints/[roberta-model_binary_20epochs_fresh.pt](http://roberta-model_binary_20epochs_fresh.pt/) --train_file new_train_annotated.json --dev_file new_dev_annotated.json --test_file doc_entities_Test_File_Created_30_11_60K_70kdisease_and_metabolites_abstracts.json --train_batch_size 2 --test_batch_size 2 --gradient_accumulation_steps 1 --num_labels 2 --learning_rate 2e-5 --classifier_lr 1e-4 --max_grad_norm 1.0 --drop_prob 0.2 --warmup_ratio 0.06 --start_steps 50000 --evaluation_steps 750 --num_train_epochs 1.0 --seed 99 --num_class 2

bash infer.sh

echo '###### Run Complete! ######'
