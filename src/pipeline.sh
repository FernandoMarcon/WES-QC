#!/bin/bash

# Load config
source config/config.sh

# Run scripts
#bash ${SRCDIR}/download_data.sh
bash ${SRCDIR}/coverage.sh

echo "Pipeline completed"