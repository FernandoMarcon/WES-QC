#!/bin/bash

# Load config
source config/config.sh

# Create directories
mkdir -p "${DATADIR}"
mkdir -p "${DATADIR}/bed"
mkdir -p "${DATADIR}/cram"
mkdir -p "${DATADIR}/ref"
mkdir -p "${DATADIR}/bam"

mkdir -p "${INTMDIR}"
mkdir -p "${INTMDIR}/bam"
mkdir -p "${INTMDIR}/coverage"
mkdir -p "${INTMDIR}/sex_estimate"
mkdir -p "${INTMDIR}/contamination"

mkdir -p "${RESDIR}"
mkdir -p "${RESDIR}/coverage"
mkdir -p "${RESDIR}/sex_estimate"
mkdir -p "${RESDIR}/contamination"
mkdir -p "${RESDIR}/reports"

mkdir -p "${PROGDIR}"
mkdir -p "${TMPDIR}"

# Download programs
wget -nc -P "${PROGDIR}" "${MOSDEPTHURL}"
chmod +x "${PROGDIR}/mosdepth"