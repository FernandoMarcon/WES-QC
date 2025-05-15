#!/bin/bash

########################################################
# Coverage
# Script to calculate the coverage of a CRAM file
########################################################

# Load config
source config/config.sh

TASK="coverage"
OUTDIR=${INTMDIR}/${TASK}/${SAMPLE}
mkdir -p ${OUTDIR}

${MOSDEPTH} --threads ${THREADS} \
    --by data/bed/${BED} \
    --fasta data/ref/${REF} \
    ${OUTDIR}/${SAMPLE} \
    data/cram/${CRAM}

python3 src/coverage_stats.py --sample ${SAMPLE} --input-dir ${OUTDIR} --output-dir ${RESDIR}/${TASK}
