# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

MODEL_DIR=../../checkpoints/RE-BC5CDR-BioGPT
MODEL=checkpoint_avg.pt
#DATA_DIR=${PWD}/../../data/BC5CDR/relis-bin
DATA_DIR=/N/project/zhangclab/Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/examples/RE-BC5CDR/../../data/BC5CDR/relis-bin
BASE_DATA_DIR=${DATA_DIR%/*}
BIN_DATA_DIR=${DATA_DIR##*/}
DATA_PREFIX=${BIN_DATA_DIR%-*}
RAW_DATA_DIR=${BASE_DATA_DIR}/raw
OUTPUT_FILE=generate_${MODEL}

INPUT_FILE=${RAW_DATA_DIR}/${DATA_PREFIX}_test.tok.bpe.x
OUTPUT_FILE=${MODEL_DIR}/${OUTPUT_FILE}
GOLD_FILE=${RAW_DATA_DIR}/CDR_Data/CDR.Corpus.v010516/CDR_TestSet.PubTator.txt
ENTITY_FILE=${RAW_DATA_DIR}/test.entities.json
PMID_FILE=${RAW_DATA_DIR}/${DATA_PREFIX}_test.pmid

MOSES=/N/project/zhangclab/Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/mosesdecoder
BIOGPT_FOLDER_CDR=/N/project/zhangclab/Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/examples/RE-BC5CDR

# average checkpoints
if [ ! -f "${MODEL_DIR}/${MODEL}" ]; then
    python ../../scripts/average_checkpoints.py --inputs=${MODEL_DIR} --output=${MODEL_DIR}/${MODEL} --num-epoch-checkpoints=5
fi

# inference
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Begin inferencing ${INPUT_FILE} using ${MODEL_DIR}/${MODEL}"
    python ../../inference.py --data_dir=${DATA_DIR} --model_dir=${MODEL_DIR} --model_file=${MODEL} --src_file=${INPUT_FILE} --output_file=${OUTPUT_FILE}
fi

# debpe
sed -i "s/@@ //g" ${OUTPUT_FILE}
# detok
perl ${MOSES}/scripts/tokenizer/detokenizer.perl -l en -a < ${OUTPUT_FILE} > ${OUTPUT_FILE}.detok



### do later
# postprocess
python postprocess.py ${OUTPUT_FILE}.detok ${ENTITY_FILE} ${PMID_FILE}
# eval
cd ${RAW_DATA_DIR}/BC5CDR_Evaluation-0.0.3
#bash eval_relation.sh PubTator ${OLDPWD}/${GOLD_FILE} ${OLDPWD}/${OUTPUT_FILE}.detok.extracted.PubTator
bash eval_relation.sh PubTator ${GOLD_FILE} ${BIOGPT_FOLDER_CDR}/${OUTPUT_FILE}.detok.extracted.PubTator
cd ${BIOGPT_FOLDER}

#test??
