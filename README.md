# Whole Exome Sequencing - Quality Control

Setup conda enviroment:
```Shell
conda config --add channels bioconda
conda config --add channels conda-forge

conda activate wesqc
conda install pandas matplotlib
conda install -c bioconda verifybamid2 mosdepth
```

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
  - download_data.sh
  - coverage.sh
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
- [x] download data
  - [x] bam
  - [x] cram
  - [x] ref
- [ ] Coverage
- [ ] Sex estimation
- [ ] Contamination
- [ ] Generate reports


## Notes
### Coverage Analysis

**Calculate depth**
- using mosdepth, instead of `samtools depth`
- output files:
  - *{SAMPLE}.per-base.bed.gz*: contains per-base coverage information
  - *{SAMPLE}.regions.bed.gz*: contains coverage statistics per region/gene

**Average Depth Across All Regions**
- can calculate this from the `regions.bed.gz` file
  - already contains mean coverage per region
  - the 4th column contains the mean coverage for each regoion

In the `*.regions.bed.gz` file, each line contains:

| Column | Description                |
| ------ | -------------------------- |
| \$1    | Chromosome                 |
| \$2    | Start position             |
| \$3    | End position               |
| \$4    | Average depth (per region) |

Let:

* $$d_i = \text{\$4}$$ (average depth in the region)
* $$l_i = \text{\$3} - \text{\$2}$$ (length of the region)
* $n$ = number of regions (number of lines in file)

$$
\text{Average Depth} = \frac{\sum_{i=1}^{n} d_i \cdot l_i}{\sum_{i=1}^{n} l_i}
= \frac{\sum_{i=1}^{n} \text{\$4} \cdot (\text{\$3} - \text{\$2})}{\sum_{i=1}^{n} (\text{\$3} - \text{\$2})}
$$

**Percentage of Bases Covered at ≥10x and ≥30x**

In the `*.per-base.bed.gz` file, each line corresponds to a base range (usually 1 base), and contains:

| Column | Description                      |
| ------ | -------------------------------- |
| \$1    | Chromosome                       |
| \$2    | Start position (0-based)         |
| \$3    | End position (typically \$2 + 1) |
| \$4    | Coverage at that base            |

Let:

* $$b_i = \text{\$3} - \text{\$2}$$ (number of bases, typically 1)
* $$c_i = \text{\$4}$$ (coverage at that position)
* $T = \sum b_i$ (total bases)
* $C_{10} = \sum b_i$ where $c_i \geq 10$
* $C_{30} = \sum b_i$ where $c_i \geq 30$

Then:

$$
\text{Percent Covered ≥10x} = \left( \frac{C_{10}}{T} \right) \times 100
\quad \text{where } C_{10} = \sum_{i, \, \text{\$4} \geq 10} (\text{\$3} - \text{\$2})
$$

$$
\text{Percent Covered ≥30x} = \left( \frac{C_{30}}{T} \right) \times 100
\quad \text{where } C_{30} = \sum_{i, \, \text{\$4} \geq 30} (\text{\$3} - \text{\$2})
$$

### Contamination Estimation
- run with [VerifyBamID](https://github.com/Griffan/VerifyBamID)
- 