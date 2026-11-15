"""Web interface for the TPM calculator.

The "business logic" (compute_tpm, parse_counts) comes from tpm.py,
this file only adds the web page around it.

Usage:
    python tpm_web.py
then open http://127.0.0.1:5000/ in the browser.
Press Ctrl-C to stop it.
"""

import os

from flask import Flask, render_template_string, request

from tpm import compute_tpm, parse_counts

app = Flask(__name__)

EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), "counts.csv")

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>TPM calculator</title>
  <style>
    body { font-family: sans-serif; max-width: 900px; margin: 30px auto; padding: 0 16px; color: #222; }
    h1 { color: #127E87; }
    textarea { width: 100%; height: 200px; font-family: monospace; }
    button { background: #127E87; color: white; border: none; padding: 8px 20px; border-radius: 6px; cursor: pointer; }
    table { border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #ccc; padding: 4px 12px; text-align: right; }
    th:first-child, td:first-child { text-align: left; }
    th { background: #edf8f7; }
    .error { color: #b00020; font-weight: bold; }
  </style>
</head>
<body>
  <h1>TPM calculator</h1>
  <p>Paste RNA-seq read counts as CSV (columns: <code>gene,length,sample1,sample2,...</code>,
     length in base pairs) or upload a CSV file, and get TPM (Transcripts Per Million) values.</p>

  <form method="post" enctype="multipart/form-data">
    <textarea name="data">{{ data }}</textarea>
    <p>or upload a file: <input type="file" name="file" accept=".csv"></p>
    <button type="submit">Calculate TPM</button>
  </form>

  {% if error %}<p class="error">{{ error }}</p>{% endif %}

  {% if rows %}
  <table>
    <tr><th>gene</th>{% for s in samples %}<th>{{ s }}</th>{% endfor %}</tr>
    {% for gene, values in rows %}
    <tr><td>{{ gene }}</td>{% for v in values %}<td>{{ "%.1f"|format(v) }}</td>{% endfor %}</tr>
    {% endfor %}
    <tr><th>total</th>{% for t in totals %}<th>{{ "%.0f"|format(t) }}</th>{% endfor %}</tr>
  </table>
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    with open(EXAMPLE_FILE) as fh:
        data = fh.read()
    samples, rows, totals, error = [], [], [], None

    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            data = uploaded.read().decode("utf-8")
        else:
            data = request.form.get("data", "")

        try:
            genes, lengths, counts = parse_counts(data.strip().splitlines())
            tpm = {sample: compute_tpm(values, lengths) for sample, values in counts.items()}
            samples = list(tpm)
            rows = [(gene, [tpm[s][i] for s in samples]) for i, gene in enumerate(genes)]
            totals = [sum(tpm[s]) for s in samples]
        except Exception as err:
            error = f"Could not read the data: {err}"

    return render_template_string(PAGE, data=data, samples=samples, rows=rows, totals=totals, error=error)


if __name__ == "__main__":
    app.run(debug=True)
