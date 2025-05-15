import pandas as pd

# get sample and regions_dir from command line
# ex: python coverage_stats_oai.py -s|--sample NA06994 -i|--input-dir intermediate/coverage/sample -o|--output-dir results/coverage

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate coverage statistics')
    parser.add_argument('-s', '--sample', type=str, required=True, help='Sample name')
    parser.add_argument('-i', '--input-dir', type=str, default="intermediate/coverage", help='Input directory')
    parser.add_argument('-o', '--output-dir', type=str, default="results/coverage", help='Output directory')
    return parser.parse_args()


args        = parse_arguments()
sample      = args.sample
regions_dir = args.input_dir
output_dir  = args.output_dir

regions_file = f"{regions_dir}/{sample}.regions.bed.gz"

# Load the mosdepth regions file (gzipped BED with mean depth per region)
df = pd.read_csv(regions_file, sep='\t', header=None, compression='gzip')

# Extract coverage and region lengths
coverage = df.iloc[:, -1].astype(float)        # last column = mean depth
start = df.iloc[:, 1].astype(int)
end   = df.iloc[:, 2].astype(int)
lengths = end - start

# Total exonic bases
total_bases = lengths.sum()

# Compute mean coverage (weighted by region length)
mean_depth = (coverage * lengths).sum() / total_bases

# Compute percentage of bases with coverage >=10x and >=30x
bases_10 = lengths[coverage >= 10].sum()
bases_30 = lengths[coverage >= 30].sum()
pct10 = bases_10 / total_bases * 100
pct30 = bases_30 / total_bases * 100

# Save the summary to a file
with open(f"{output_dir}/{sample}.coverage_stats.txt", "w") as f:
    f.write(f"Mean coverage (exonic): {mean_depth:.2f}\n")
    f.write(f"% bases >= 10x: {pct10:.2f}%\n")
    f.write(f"% bases >= 30x: {pct30:.2f}%\n")