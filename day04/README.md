# Day 04 – A web interface for the TPM calculator

I took my [day03](../day03/) program (TPM normalization of RNA-seq read counts),
copied it here so the old version stays untouched, and added a web application
with [Flask](https://flask.palletsprojects.com/).

## Files

- [tpm.py](tpm.py) – the "business logic", copied from day03. It still works on the command line.
  The only change: reading the CSV was split into `parse_counts(lines)` (works on any lines of text)
  and `read_counts(filename)` (opens a file and calls `parse_counts`), so the web app can use
  the same code for data that comes from the browser.
- [tpm_web.py](tpm_web.py) – the Flask web application. It imports `compute_tpm` and `parse_counts`
  from `tpm.py` and only adds the web page around them.
- [counts.csv](counts.csv) – the example data (made-up counts), shown pre-filled on the page.

## How to run

Install Flask once:

```
pip install flask
```

Command line (old system):

```
python day04/tpm.py
```

Web application (new system):

```
cd day04
python tpm_web.py
```

Then open http://127.0.0.1:5000/ in the browser. Press `Ctrl-C` in the terminal to stop it.

On the page you can:

- click **Calculate TPM** to use the example data,
- edit / paste your own CSV (`gene,length,sample1,sample2,...`), or
- upload a CSV file.

The result is shown as a table, with a "total" row that is always 1,000,000 per sample.
If the data has a mistake (e.g. text instead of a number) the page shows an error message.

## Checking that both systems work

- `python day03/tpm.py` and `python day04/tpm.py` print the same table.
- The web page shows the same numbers (e.g. IL6 in treated_1 = 23341.7).
- Small example to check by hand – genes A (1000 bp) and B (2000 bp) with 100 reads each give
  TPM 666,666.7 and 333,333.3: same reads, but B is twice as long.

## Tests (day 5 assignment)

I added automated tests with [pytest](https://pytest.org/):

- [test_tpm.py](test_tpm.py) – tests for the business logic:
  - `compute_tpm`: the A/B example worked out by hand, the TPM always sums to 1,000,000,
    genes with the same length are proportional to their counts, sequencing a sample deeper
    gives the same TPM, a single gene gets 1,000,000, a 0 count gives 0 TPM, and all-zero
    counts raise `ZeroDivisionError`.
  - `parse_counts` / `read_counts`: reading genes, lengths and samples (in the right order),
    a `ValueError` for text instead of a number, and the example `counts.csv` file
    (including the IL6 value the web page shows).
- [test_tpm_web.py](test_tpm_web.py) – tests for the web page using Flask's test client
  (no real server needed): the page loads with the example data, calculating from pasted text
  and from an uploaded file, and that bad or empty data shows an error message instead of crashing.

Install pytest once and run the tests from the root of the repository:

```
pip install pytest
python -m pytest day04 -v
```

Result: `17 passed`.

To check that the tests really catch mistakes, I temporarily removed the gene-length
correction from `compute_tpm` – 4 tests failed – and then put it back.

Prompt: "Write pytest tests for the business logic of my day04 TPM program (compute_tpm,
parse_counts, read_counts) and for the Flask web page, and put them in day04."

## Other changes

- Added a `.gitignore` in the root of the repository so the `__pycache__` folder Python creates
  is not committed.

## Prompts I used

- "Take my day03 TPM program, copy it to day04, and write a Flask web application that uses
  compute_tpm from it. The page should let me paste CSV data or upload a file and show the TPM
  values as a table. Keep the command line version working."
