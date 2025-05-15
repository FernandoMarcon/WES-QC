#!/bin/bash

# =======================================================
# Contamination Analysis
# Script to estimate DNA contamination using VerifyBamID
# =======================================================

source config/config.sh

TASK="contamination"
OUTDIR=${RESDIR}/${TASK}/${SAMPLE}
mkdir -p $OUTDIR

SVD_DIR="${HOME}/miniconda3/envs/wesqc/share/verifybamid2-2.0.1-12"
verifybamid2 \
  --SVDPrefix "${SVD_DIR}/resource/1000g.phase3.100k.b38.vcf.gz.dat" \
  --Reference data/ref/$REF \
  --BamFile data/cram/$CRAM \
  --BedPath data/bed/$BED \
  --NumThread $THREADS \
  --Output $OUTDIR/${SAMPLE}


# Check if VerifyBamID ran successfully
if [ $? -eq 0 ]; then
  echo "VerifyBamID analysis completed successfully. Results are in $VERIFYBAMID_PREFIX.*"
else
  echo "Error: VerifyBamID analysis failed."
  exit 1
fi