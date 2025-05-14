#! /bin/bash
SAMPLE="NA06994"

# BED
BED_URL="https://www.twistbioscience.com/sites/default/files/resources/2022-12/"
BED="hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed"

echo "Downloading BED file..."
wget -nc -P data/bed $BED_URL/$BED

# REF
REF_URL="ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome"
REF="GRCh38_full_analysis_set_plus_decoy_hla"

echo "Downloading reference genome..."
wget -nc -P data/ref $REF_URL/$REF{.fa,.fa.fai,.dict}

# CRAM
CRAM_URL="http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/data/CEU/${SAMPLE}/exome_alignment"
CRAM="${SAMPLE}.alt_bwamem_GRCh38DH.20150826.CEU.exome"

echo "Downloading CRAM/CRAI files..."
wget -nc -P data/cram $CRAM_URL/$CRAM{.cram,.cram.crai}