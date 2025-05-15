#!/bin/bash

# Load config
source config/config.sh

# Run scripts
#bash ${SRCDIR}/download_data.sh

# Coverage analysis
bash "src/coverage.sh"  
# python3 src/coverage_stats.py --sample ${SAMPLE} --input-dir "intermediate/coverage/" --output-dir "results/coverage/"

# Sex inference
python3 src/estimate_sex.py -s ${SAMPLE} -i "intermediate/coverage/" -o "results/sex_inference/"

# Contamination estimation
bash src/contamination.sh

echo "Pipeline completed"