# Whole Exome Sequencing - Quality Control

## Overview
1. ​Genomic coverage calculation;
2. ​Inference of genetic sex from sequencing data;
3. ​Estimation of contamination by exogenous DNA or from other individuals.

### Tasks
1. **Conversion of CRAM file** to an appropriate format (BAM or FASTQ), if necessary. CRAM can be used directly, without conversion, according to your design choices;
2. **Calculation of coverage** in exonic regions (from the BED file), including:
   1. Average depth;
   2. Percentage of the exome covered at least 10x and 30x;
3. **Inference of genetic sex**, based on coverage of X and Y chromosomes. Use preexisting tools or implement your own solution;
4. **Estimation of contamination**, select the appropriate tools and justify your choice in the README;
5. **Report Generation**. Generation of textual and/or graphical reports with the results;
6. **Automation**. Automation of the pipeline via Bash scripts, Makefile, Snakemake or Nextflow (your choice).

### Workflow
1. Get data
2. Coverage
3. Sex estimation
4. Contamination
5. Generate reports

### Project Structure
data
  - cram/
  - bed/
  - ref/
- intermediate/
  - bam/
  - coverage/
  - sex_estimation/
  - contamination/
- results/
  - coverage/
  - sex_estimation/
  - contamination/
  - reports/
- config/
  - config.yaml
- src/
- logs/

## Dataset for Tests
Public WES  data from 1kGenomes ([link](http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/data/CEU/NA06994/exome_alignment/))

CRAM files:
- NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram ()
- NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram.crai​

BED file:
- https://www.twistbioscience.com/resources/data-files/twist-exome-20-bed-files ​

MD5 hashes for integrity check:
- cram: 3d8d8dc27d85ceaf0daefa493b8bd660
- crai: 15a6576f46f51c37299fc004ed47fcd9
- bed: c3a7cea67f992e0412db4b596730d276

## TODO
- [x] [script] download data
  - [x] bam
  - [x] cram
  - [x] ref
- [ ] Coverage
- [ ] Sex estimation
- [ ] Contamination
- [ ] Generate reports