# -*- coding: utf-8 -*-
"""quiz2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HFCl2WnOISZ_vW8OD9VSM6Ig5rRvfc8i
"""

import os

# Verify that the files were uploaded
print("Checking if files exist...")
print("RNA-sequence1.fna exists:", os.path.exists("/content/RNA-sequence1.fna"))
print("RNA-sequence2.fna exists:", os.path.exists("/content/RNA-sequence2.fna"))

def read_fasta(file_path):
    """Reads an RNA sequence from a FASTA file, ignoring header lines (>)"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return ''.join(line.strip() for line in lines if not line.startswith('>'))

# Read RNA sequences from the files
rna_seq1 = read_fasta("/content/RNA-sequence1.fna")
rna_seq2 = read_fasta("/content/RNA-sequence2.fna")

# Print first 100 bases for verification
print("RNA Sequence 1 (first 100 bases):", rna_seq1[:100])
print("RNA Sequence 2 (first 100 bases):", rna_seq2[:100])

def reverse_transcribe(rna_sequence):
    """Converts RNA sequence to DNA sequence by replacing Uracil (U) with Thymine (T)."""
    return rna_sequence.replace('U', 'T')

# Convert RNA to DNA
dna_seq1 = reverse_transcribe(rna_seq1)
dna_seq2 = reverse_transcribe(rna_seq2)

# Print first 100 bases
print("DNA Sequence 1 (first 100 bases):", dna_seq1[:100])
print("DNA Sequence 2 (first 100 bases):", dna_seq2[:100])

from collections import Counter

def count_nucleotide_frequencies(sequence, k):
    """Counts absolute and percentage frequency of k-nucleotides in a sequence."""
    kmer_counts = Counter([sequence[i:i+k] for i in range(len(sequence)-k+1)])
    total_kmers = sum(kmer_counts.values())
    percentage_frequencies = {k: (v / total_kmers) * 100 for k, v in kmer_counts.items()}
    return kmer_counts, percentage_frequencies

# Compute dinucleotide and trinucleotide frequencies
di_counts1, di_percent1 = count_nucleotide_frequencies(rna_seq1, 2)
di_counts2, di_percent2 = count_nucleotide_frequencies(rna_seq2, 2)

tri_counts1, tri_percent1 = count_nucleotide_frequencies(rna_seq1, 3)
tri_counts2, tri_percent2 = count_nucleotide_frequencies(rna_seq2, 3)

# Display first few dinucleotide frequencies
print("Sample dinucleotide frequencies (Seq1):", list(di_percent1.items())[:5])
print("Sample trinucleotide frequencies (Seq1):", list(tri_percent1.items())[:5])

def compare_frequencies(freq1, freq2):
    """Identifies k-mers with a 3x difference in percentage between sequences."""
    significant_differences = {}
    for kmer in set(freq1.keys()).union(set(freq2.keys())):
        if kmer in freq1 and kmer in freq2:
            ratio = max(freq1[kmer], freq2[kmer]) / max(1e-6, min(freq1[kmer], freq2[kmer]))
            if ratio >= 3:
                significant_differences[kmer] = (freq1.get(kmer, 0), freq2.get(kmer, 0))
    return significant_differences

# Find significant differences (3x variation)
significant_di_diffs = compare_frequencies(di_percent1, di_percent2)
significant_tri_diffs = compare_frequencies(tri_percent1, tri_percent2)

# Print significant differences
print("\nSignificant Dinucleotide Differences (3x or more):", significant_di_diffs)
print("\nSignificant Trinucleotide Differences (3x or more):", significant_tri_diffs)

import pandas as pd

# Convert to Pandas DataFrames for better readability
di_freq_df = pd.DataFrame(list(di_percent1.items()), columns=["Dinucleotide", "Seq1_Percentage"])
di_freq_df["Seq2_Percentage"] = di_freq_df["Dinucleotide"].map(di_percent2).fillna(0)

tri_freq_df = pd.DataFrame(list(tri_percent1.items()), columns=["Trinucleotide", "Seq1_Percentage"])
tri_freq_df["Seq2_Percentage"] = tri_freq_df["Trinucleotide"].map(tri_percent2).fillna(0)

significant_di_df = pd.DataFrame(list(significant_di_diffs.items()), columns=["Dinucleotide", "Percentages (Seq1, Seq2)"])
significant_tri_df = pd.DataFrame(list(significant_tri_diffs.items()), columns=["Trinucleotide", "Percentages (Seq1, Seq2)"])

# Display tables
print("\nDinucleotide Frequencies:")
display(di_freq_df.head())

print("\nTrinucleotide Frequencies:")
display(tri_freq_df.head())

print("\nSignificant Dinucleotide Differences (3x or more):")
display(significant_di_df)

print("\nSignificant Trinucleotide Differences (3x or more):")
display(significant_tri_df)

# Save results as CSV files
di_freq_df.to_csv("/content/Dinucleotide_Frequencies.csv", index=False)
tri_freq_df.to_csv("/content/Trinucleotide_Frequencies.csv", index=False)
significant_di_df.to_csv("/content/Significant_Dinucleotide_Differences.csv", index=False)
significant_tri_df.to_csv("/content/Significant_Trinucleotide_Differences.csv", index=False)

print("Files saved successfully. Download them from the Files tab.")

# Save Python script as RNA_Analysis.py
script_content = """\
from collections import Counter
import pandas as pd

def read_fasta(file_path):
    \"\"\"Reads an RNA sequence from a FASTA file, ignoring header lines (>)\"\"\"
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return ''.join(line.strip() for line in lines if not line.startswith('>'))

def reverse_transcribe(rna_sequence):
    \"\"\"Converts RNA sequence to DNA sequence by replacing Uracil (U) with Thymine (T).\"\"\"
    return rna_sequence.replace('U', 'T')

def count_nucleotide_frequencies(sequence, k):
    \"\"\"Counts absolute and percentage frequency of k-nucleotides in a sequence.\"\"\"
    kmer_counts = Counter([sequence[i:i+k] for i in range(len(sequence)-k+1)])
    total_kmers = sum(kmer_counts.values())
    percentage_frequencies = {k: (v / total_kmers) * 100 for k, v in kmer_counts.items()}
    return kmer_counts, percentage_frequencies

def compare_frequencies(freq1, freq2):
    \"\"\"Identifies k-mers with a 3x difference in percentage between sequences.\"\"\"
    significant_differences = {}
    for kmer in set(freq1.keys()).union(set(freq2.keys())):
        if kmer in freq1 and kmer in freq2:
            ratio = max(freq1[kmer], freq2[kmer]) / max(1e-6, min(freq1[kmer], freq2[kmer]))
            if ratio >= 3:
                significant_differences[kmer] = (freq1.get(kmer, 0), freq2.get(kmer, 0))
    return significant_differences

# Load RNA sequences from files
rna_file1 = "/content/RNA-sequence1.fna"
rna_file2 = "/content/RNA-sequence2.fna"

rna_seq1 = read_fasta(rna_file1)
rna_seq2 = read_fasta(rna_file2)

# Reverse Transcription (RNA → DNA)
dna_seq1 = reverse_transcribe(rna_seq1)
dna_seq2 = reverse_transcribe(rna_seq2)

# Compute nucleotide frequencies
di_counts1, di_percent1 = count_nucleotide_frequencies(rna_seq1, 2)
di_counts2, di_percent2 = count_nucleotide_frequencies(rna_seq2, 2)

tri_counts1, tri_percent1 = count_nucleotide_frequencies(rna_seq1, 3)
tri_counts2, tri_percent2 = count_nucleotide_frequencies(rna_seq2, 3)

# Identify 3x significant differences
significant_di_diffs = compare_frequencies(di_percent1, di_percent2)
significant_tri_diffs = compare_frequencies(tri_percent1, tri_percent2)

# Save results as CSV files
di_freq_df = pd.DataFrame(list(di_percent1.items()), columns=["Dinucleotide", "Seq1_Percentage"])
di_freq_df["Seq2_Percentage"] = di_freq_df["Dinucleotide"].map(di_percent2).fillna(0)
di_freq_df.to_csv("/content/Dinucleotide_Frequencies.csv", index=False)

tri_freq_df = pd.DataFrame(list(tri_percent1.items()), columns=["Trinucleotide", "Seq1_Percentage"])
tri_freq_df["Seq2_Percentage"] = tri_freq_df["Trinucleotide"].map(tri_percent2).fillna(0)
tri_freq_df.to_csv("/content/Trinucleotide_Frequencies.csv", index=False)

significant_di_df = pd.DataFrame(list(significant_di_diffs.items()), columns=["Dinucleotide", "Percentages (Seq1, Seq2)"])
significant_di_df.to_csv("/content/Significant_Dinucleotide_Differences.csv", index=False)

significant_tri_df = pd.DataFrame(list(significant_tri_diffs.items()), columns=["Trinucleotide", "Percentages (Seq1, Seq2)"])
significant_tri_df.to_csv("/content/Significant_Trinucleotide_Differences.csv", index=False)

print("✅ RNA Analysis Completed. Files Saved Successfully.")
"""

# Write the script to a file
with open("/content/RNA_Analysis.py", "w") as f:
    f.write(script_content)

print("✅ Python script saved as RNA_Analysis.py. Download it from the Files tab.")