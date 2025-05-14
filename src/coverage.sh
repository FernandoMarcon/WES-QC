#!/bin/bash

########################################################
# Coverage
# Script to calculate the coverage of a CRAM file
########################################################

# Load config
source config/config.sh

# Create output directories
mkdir -p ${INTMDIR}/coverage
mkdir -p ${OUTDIR}/coverage

echo "Calculating coverage statistics for ${SAMPLE}..."

# Calculate coverage using samtools depth
# -b option to limit analysis to regions in BED file
samtools depth -b ${DATADIR}/bed/${BED} \
              ${DATADIR}/cram/${CRAM} \
              -r ${DATADIR}/ref/${REF} > ${INTMDIR}/coverage/${SAMPLE}.depth

# Calculate average depth
echo "Calculating average depth..."
AVG_DEPTH=$(awk '{sum+=$3} END {print sum/NR}' ${INTMDIR}/coverage/${SAMPLE}.depth)

# Calculate coverage at different thresholds (10x and 30x)
echo "Calculating coverage at 10x and 30x..."
TOTAL_POSITIONS=$(wc -l < ${INTMDIR}/coverage/${SAMPLE}.depth)
COV_10X=$(awk '$3>=10 {count++} END {print (count/NR)*100}' ${INTMDIR}/coverage/${SAMPLE}.depth)
COV_30X=$(awk '$3>=30 {count++} END {print (count/NR)*100}' ${INTMDIR}/coverage/${SAMPLE}.depth)

# Generate report
echo "Generating coverage report..."
cat << EOF > ${OUTDIR}/coverage/${SAMPLE}_coverage_report.txt
Coverage Statistics for ${SAMPLE}
================================
Average depth: ${AVG_DEPTH}x
Percentage covered at ≥10x: ${COV_10X}%
Percentage covered at ≥30x: ${COV_30X}%
EOF

echo "Coverage analysis completed. Results saved in ${OUTDIR}/coverage/${SAMPLE}_coverage_report.txt"

