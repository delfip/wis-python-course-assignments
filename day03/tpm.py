"""Compute TPM (Transcripts Per Million) from RNA-seq read counts.

TPM corrects raw read counts for two things:
  1. gene length   - longer genes get more reads just because they are longer
  2. sequencing depth - some samples are sequenced more deeply than others

For each sample:
  rate_i = count_i / (length_i in kilobases)
  TPM_i  = rate_i / sum(all rates) * 1,000,000

So the TPM values in every sample add up to 1,000,000,
which makes samples comparable to each other.

Usage:
    python tpm.py                 (uses counts.csv next to this file)
    python tpm.py my_counts.csv
"""

import csv
import os
import sys


def compute_tpm(counts, lengths):
    """Return a list of TPM values.

    counts  -- list of read counts, one per gene
    lengths -- list of gene lengths in base pairs, same order as counts
    """
    rates = [count / (length / 1000) for count, length in zip(counts, lengths)]
    total = sum(rates)
    return [rate / total * 1_000_000 for rate in rates]


def read_counts(filename):
    """Read the CSV file and return (genes, lengths, {sample: counts})."""
    with open(filename, newline="") as fh:
        reader = csv.DictReader(fh)
        samples = reader.fieldnames[2:]  # columns after gene and length
        genes, lengths = [], []
        counts = {sample: [] for sample in samples}
        for row in reader:
            genes.append(row["gene"])
            lengths.append(int(row["length"]))
            for sample in samples:
                counts[sample].append(int(row[sample]))
    return genes, lengths, counts


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = os.path.join(os.path.dirname(__file__), "counts.csv")

    genes, lengths, counts = read_counts(filename)
    tpm = {sample: compute_tpm(values, lengths) for sample, values in counts.items()}

    samples = list(tpm)
    print("gene".ljust(10) + "".join(s.rjust(12) for s in samples))
    for i, gene in enumerate(genes):
        print(gene.ljust(10) + "".join(f"{tpm[s][i]:12.1f}" for s in samples))
    print("total".ljust(10) + "".join(f"{sum(tpm[s]):12.0f}" for s in samples))


if __name__ == "__main__":
    main()
