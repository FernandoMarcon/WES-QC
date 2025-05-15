#!/usr/bin/env python3

import argparse
import os
import pandas as pd

def estimate_sex_from_mosdepth(sample, input_dir='intermediate/coverage/', outdir='results/sex_inference/',
                               x_female_high=0.8, y_female_low=0.2,
                               x_male_low=0.6, y_male_high=0.2,
                               chr_format='chr'):
    """
    Estimates biological sex based on mosdepth coverage output for X and Y chromosomes.

    Args:
        sample (str): Sample name.
        input_dir (str, optional): Directory containing mosdepth output files.
                                     Defaults to 'intermediate/coverage/'.
        outdir (str, optional): Directory to store the final report.
                                Defaults to 'results/sex_inference/'.
        x_female_high (float, optional): Upper threshold for X/autosome ratio to classify as female. Defaults to 0.8.
        y_female_low (float, optional): Lower threshold for Y/autosome ratio to classify as female. Defaults to 0.2.
        x_male_low (float, optional): Lower threshold for X/autosome ratio to classify as male. Defaults to 0.6.
        y_male_high (float, optional): Upper threshold for Y/autosome ratio to classify as male. Defaults to 0.2.
        chr_format (str, optional): Format of chromosome names in mosdepth summary ('chr' or '').
                                     Defaults to 'chr'.
    Usage:
        # Using Default Thresholds and "chr" format (same as before):
        python estimate_sex.py -s NA06994 -i intermediate/coverage/ -o results/sex_inference/

        # Changing Thresholds:
        python estimate_sex.py -s NA06994 -i intermediate/coverage/ -o results/sex_inference/ --x_female_high 0.9 --y_male_high 0.1

        # Using "X" and "Y" chromosome names in the mosdepth output:
        python estimate_sex.py -s NA06994 -i intermediate/coverage/ -o results/sex_inference/ 
    """
    summary_file = os.path.join(input_dir, sample, f"{sample}.mosdepth.summary.txt")
    report_file = os.path.join(outdir, f"{sample}_sex_estimate.txt")

    x_chr = f"{chr_format}X"
    y_chr = f"{chr_format}Y"

    if not os.path.exists(summary_file):
        print(f"Error: Mosdepth summary file not found at {summary_file}")
        return

    try:
        df = pd.read_csv(summary_file, sep='\t', index_col='chrom')
    except Exception as e:
        print(f"Error reading mosdepth summary file: {e}")
        return

    if x_chr not in df.index or y_chr not in df.index:
        print(f"Error: Could not find coverage information for chromosomes {x_chr} and {y_chr} in the mosdepth summary.")
        print(f"Available chromosomes in summary: {df.index.tolist()}")
        return

    x_coverage = df.loc[x_chr, 'mean']
    y_coverage = df.loc[y_chr, 'mean']

    # Assuming autosome coverage can be approximated by the average coverage
    # of all autosomal chromosomes (excluding X and Y).
    autosome_coverage = df[~df.index.isin([x_chr, y_chr])]['mean'].mean()

    if autosome_coverage == 0:
        print("Error: Could not determine autosome coverage.")
        return

    x_ratio = x_coverage / autosome_coverage if autosome_coverage > 0 else 0
    y_ratio = y_coverage / autosome_coverage if autosome_coverage > 0 else 0

    # Heuristic for sex determination based on coverage ratios with externalized thresholds
    if x_ratio > x_female_high and y_ratio < y_female_low:
        predicted_sex = "Female (XX)"
        confidence = "High"
    elif x_ratio < x_male_low and y_ratio > y_male_high:
        predicted_sex = "Male (XY)"
        confidence = "High"
    elif x_ratio > x_male_low and y_ratio > y_female_low:
        predicted_sex = "Likely Female or potential aneuploidy (e.g., XXY)"
        confidence = "Medium"
    elif x_ratio < x_female_high and y_ratio < y_male_high:
        predicted_sex = "Likely Male or potential aneuploidy (e.g., X0)"
        confidence = "Medium"
    else:
        predicted_sex = "Indeterminate"
        confidence = "Low"

    # Create output directory if it doesn't exist
    os.makedirs(outdir, exist_ok=True)

    with open(report_file, 'w') as outfile:
        outfile.write(f"Sample: {sample}\n")
        outfile.write(f"{x_chr} Chromosome Coverage: {x_coverage:.2f}\n")
        outfile.write(f"{y_chr} Chromosome Coverage: {y_coverage:.2f}\n")
        outfile.write(f"Average Autosome Coverage: {autosome_coverage:.2f}\n")
        outfile.write(f"{x_chr}/Autosome Coverage Ratio: {x_ratio:.2f}\n")
        outfile.write(f"{y_chr}/Autosome Coverage Ratio: {y_ratio:.2f}\n")
        outfile.write(f"Predicted Sex: {predicted_sex}\n")
        outfile.write(f"Confidence: {confidence}\n")

    print(f"Sex estimation for {sample} complete. Results saved to {report_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate biological sex from mosdepth coverage output.")
    parser.add_argument("-s", "--sample", required=True, help="Sample name")
    parser.add_argument("-i", "--input-dir", default="intermediate/coverage/", help="Directory with mosdepth outputs")
    parser.add_argument("-o", "--outdir", default="results/sex_inference/", help="Output directory for the report")
    parser.add_argument("--x_female_high", type=float, default=0.8, help="Upper threshold for X/autosome ratio (female)")
    parser.add_argument("--y_female_low", type=float, default=0.2, help="Lower threshold for Y/autosome ratio (female)")
    parser.add_argument("--x_male_low", type=float, default=0.6, help="Lower threshold for X/autosome ratio (male)")
    parser.add_argument("--y_male_high", type=float, default=0.2, help="Upper threshold for Y/autosome ratio (male)")
    parser.add_argument("--chr_format", default="chr", choices=['chr', ''], help="Chromosome name format in mosdepth summary ('chr' or '')")

    args = parser.parse_args()

    estimate_sex_from_mosdepth(args.sample, args.input_dir, args.outdir,
                               args.x_female_high, args.y_female_low,
                               args.x_male_low, args.y_male_high,
                               args.chr_format)