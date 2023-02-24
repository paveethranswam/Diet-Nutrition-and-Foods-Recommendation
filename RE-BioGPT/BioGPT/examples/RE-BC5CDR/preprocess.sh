# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

DATA_DIR=../../data/BC5CDR
prefix=relis
RAW_DATA_DIR=${DATA_DIR}/raw
OUTPUT_DIR=${DATA_DIR}/${prefix}-bin

if [ -d "${OUTPUT_DIR}" ]; then
    rm -rf ${OUTPUT_DIR}
fi

python rebuild_data.py ${RAW_DATA_DIR}

cp ${DATA_DIR}/../dict.txt ${RAW_DATA_DIR}/
cp ${DATA_DIR}/../bpecodes ${RAW_DATA_DIR}/

SPLIT=(train valid test)

for ff in ${SPLIT[@]}; do
    if [ -f "${RAW_DATA_DIR}/${prefix}_$ff.y" ]; then
        echo "Preprocessing ${ff}"

        perl /N/u/paswam/Carbonate/Desktop/Link\ to\ Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en -a -threads 8 < ${RAW_DATA_DIR}/${prefix}_$ff.x > ${RAW_DATA_DIR}/${prefix}_$ff.tok.x
        perl /N/u/paswam/Carbonate/Desktop/Link\ to\ Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en -a -threads 8 < ${RAW_DATA_DIR}/${prefix}_$ff.y > ${RAW_DATA_DIR}/${prefix}_$ff.tok.y

        /N/u/paswam/Carbonate/Desktop/Link\ to\ Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/fastBPE/fast applybpe ${RAW_DATA_DIR}/${prefix}_$ff.tok.bpe.x ${RAW_DATA_DIR}/${prefix}_$ff.tok.x ${RAW_DATA_DIR}/bpecodes
        /N/u/paswam/Carbonate/Desktop/Link\ to\ Pavi/Jack/Diet-Nutrition-and-Foods-Recommendation/RE-BioGPT/BioGPT/fastBPE/fast applybpe ${RAW_DATA_DIR}/${prefix}_$ff.tok.bpe.y ${RAW_DATA_DIR}/${prefix}_$ff.tok.y ${RAW_DATA_DIR}/bpecodes

        rm ${RAW_DATA_DIR}/${prefix}_$ff.tok.x ${RAW_DATA_DIR}/${prefix}_$ff.tok.y
    fi
done

# do binarize
fairseq-preprocess \
    -s x -t y --workers 8 \
    --joined-dictionary \
    --trainpref ${RAW_DATA_DIR}/${prefix}_train.tok.bpe \
    --validpref ${RAW_DATA_DIR}/${prefix}_valid.tok.bpe \
    --testpref ${RAW_DATA_DIR}/${prefix}_test.tok.bpe \
    --destdir ${OUTPUT_DIR} \
    --srcdict ${RAW_DATA_DIR}/dict.txt
