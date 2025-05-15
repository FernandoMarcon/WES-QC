#!/bin/bash

# Load config
source config/config.sh

mkdir -p ${INTMDIR}/bam

TASK="cram2bam"

samtools view \
    -@ ${THREADS} \
    -T ${DATADIR}/ref/${REF} \
    -b \
    -o ${INTMDIR}/bam/${SAMPLE}.bam \
    ${DATADIR}/cram/${CRAM}

# Index BAM file
samtools index ${INTMDIR}/bam/${SAMPLE}.bam