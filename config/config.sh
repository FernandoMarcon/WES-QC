#!/bin/bash

# VARIABLES
SAMPLE="NA06994"
THREADS=10

# DIRS
DATADIR="data"
TMPDIR="tmp"
INTMDIR="intermediate"
RESDIR="results"
PROGDIR="programs"

# FILES
BED="hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed"
REF="GRCh38_full_analysis_set_plus_decoy_hla.fa"
CRAM="NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram"

# PROGRAMS
SAMTOOLS="samtools"

MOSDEPTHURL="https://github.com/brentp/mosdepth/releases/download/v0.3.11/mosdepth"
MOSDEPTH="${PROGDIR}/mosdepth"