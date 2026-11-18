"""Tests for the "business logic" in tpm.py.

Run from the repository root with:
    python -m pytest day04
"""

import os

import pytest

from tpm import compute_tpm, parse_counts, read_counts


# ---------- compute_tpm ----------

def test_example_by_hand():
    # Same reads, but gene B is twice as long -> A is twice as expressed
    # rates: A = 100 / 1 = 100, B = 100 / 2 = 50, total = 150
    assert compute_tpm([100, 100], [1000, 2000]) == pytest.approx([666_666.67, 333_333.33])


def test_sum_is_one_million():
    tpm = compute_tpm([15, 300, 7, 1200], [500, 2500, 1000, 3000])
    assert sum(tpm) == pytest.approx(1_000_000)


def test_same_length_is_proportional_to_counts():
    # When all genes have the same length, TPM only depends on the counts
    assert compute_tpm([10, 30, 60], [1500, 1500, 1500]) == pytest.approx([100_000, 300_000, 600_000])


def test_sequencing_depth_does_not_matter():
    # A sample sequenced 10 times deeper must give the same TPM
    lengths = [1000, 2000, 1500]
    assert compute_tpm([10, 20, 30], lengths) == pytest.approx(compute_tpm([100, 200, 300], lengths))


def test_single_gene_gets_everything():
    assert compute_tpm([42], [1234]) == pytest.approx([1_000_000])


def test_zero_count_gives_zero_tpm():
    tpm = compute_tpm([0, 50], [1000, 1000])
    assert tpm[0] == 0
    assert tpm[1] == pytest.approx(1_000_000)


def test_all_zero_counts_raises():
    # Nothing to normalize: dividing by a total of 0 is an error
    with pytest.raises(ZeroDivisionError):
        compute_tpm([0, 0], [1000, 2000])


# ---------- parse_counts / read_counts ----------

def test_parse_counts():
    lines = [
        "gene,length,ctrl,treated",
        "A,1000,10,20",
        "B,2000,30,40",
    ]
    genes, lengths, counts = parse_counts(lines)
    assert genes == ["A", "B"]
    assert lengths == [1000, 2000]
    assert counts == {"ctrl": [10, 30], "treated": [20, 40]}


def test_parse_counts_keeps_sample_order():
    genes, lengths, counts = parse_counts(["gene,length,z,a,m", "A,1000,1,2,3"])
    assert list(counts) == ["z", "a", "m"]


def test_parse_counts_bad_number():
    with pytest.raises(ValueError):
        parse_counts(["gene,length,s1", "A,abc,10"])


def test_read_example_file():
    filename = os.path.join(os.path.dirname(__file__), "counts.csv")
    genes, lengths, counts = read_counts(filename)
    assert len(genes) == 8
    assert genes[0] == "GAPDH"
    assert lengths[0] == 1875
    assert list(counts) == ["control_1", "control_2", "treated_1", "treated_2"]
    assert counts["treated_1"][genes.index("IL6")] == 690


def test_example_file_results():
    # The same numbers the command line and the web page show
    genes, lengths, counts = read_counts(os.path.join(os.path.dirname(__file__), "counts.csv"))
    tpm = compute_tpm(counts["treated_1"], lengths)
    assert tpm[genes.index("IL6")] == pytest.approx(23341.7, abs=0.1)
