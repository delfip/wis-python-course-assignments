# Day 03 – TPM normalization of RNA-seq counts

## The science

In RNA-seq we count how many sequencing reads map to each gene. Raw counts can't be
compared directly, because:

1. **Longer genes get more reads** just because they are longer.
2. **Samples are sequenced to different depths** (one sample may have 20M reads, another 30M).

**TPM (Transcripts Per Million)** corrects for both. For each sample:

```
rate_i = count_i / (gene length_i in kilobases)
TPM_i  = rate_i / sum(all rates) × 1,000,000
```

The TPM values in every sample add up to 1,000,000, so samples become comparable.

## Files

- [tpm.py](tpm.py) – the program. The function `compute_tpm(counts, lengths)` does the
  computation; the rest reads the CSV and prints a table.
- [counts.csv](counts.csv) – example data: 8 human genes, their length (bp) and read counts
  in 2 control and 2 treated samples. The counts are **made up** for this exercise
  (the treatment was imagined as a stress/DNA-damage response: TP53, CDKN1A and IL6 go up,
  MYC goes down; GAPDH and ACTB are housekeeping genes).

## How to run

```
python day03/tpm.py
```

or with another file with the same format (`gene,length,sample1,sample2,...`):

```
python day03/tpm.py my_counts.csv
```

Output:

```
gene         control_1   control_2   treated_1   treated_2
GAPDH         366212.8    373254.8    324591.4    328791.7
ACTB          512200.0    510490.6    449936.4    452445.9
ALB            16926.9     15447.7     77344.1     78989.8
TP53            7134.3      6822.4     20227.8     18940.3
MYC            18572.3     17896.8      5294.1      5212.1
VIM            71817.3     69230.5     63960.4     60518.5
CDKN1A          5447.1      5211.1     35304.1     33435.1
IL6             1689.3      1645.9     23341.7     21666.6
total          1000000     1000000     1000000     1000000
```

## Prompts I used

- "Write a Python program with a function that computes TPM from RNA-seq read counts and gene
  lengths. Read the data from a CSV file with columns gene, length and one column per sample,
  and print a table of TPM values. Use only the standard library and explain the formula in comments."
- "Create an example counts.csv with about 8 human genes, 2 control and 2 treated samples,
  where the treatment looks like a DNA-damage response."

## Tools

- Wrote and ran the code in VS Code with the help of an AI assistant.
- Committed and pushed with the Git (Source Control) panel in VS Code.
