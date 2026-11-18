"""Tests for the Flask web interface in tpm_web.py.

Flask's test client sends requests to the app without starting a real server.

Run from the repository root with:
    python -m pytest day04
"""

import io

import pytest

from tpm_web import app


@pytest.fixture
def client():
    return app.test_client()


def test_page_loads_with_example_data(client):
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "TPM calculator" in html
    assert "GAPDH,1875" in html  # the text box is pre-filled
    assert "<table>" not in html  # no results before clicking the button


def test_calculate_from_text(client):
    data = "gene,length,s1\nA,1000,100\nB,2000,100\n"
    html = client.post("/", data={"data": data}).get_data(as_text=True)
    assert "<td>A</td><td>666666.7</td>" in html
    assert "<td>B</td><td>333333.3</td>" in html
    assert "<th>1000000</th>" in html


def test_calculate_from_uploaded_file(client):
    upload = (io.BytesIO(b"gene,length,s1\nA,1000,100\nB,2000,100\n"), "counts.csv")
    response = client.post("/", data={"data": "", "file": upload}, content_type="multipart/form-data")
    html = response.get_data(as_text=True)
    assert "<td>A</td><td>666666.7</td>" in html


def test_bad_data_shows_error(client):
    response = client.post("/", data={"data": "gene,length,s1\nA,abc,10"})
    assert response.status_code == 200  # the page does not crash
    assert "Could not read the data" in response.get_data(as_text=True)


def test_empty_data_shows_error(client):
    response = client.post("/", data={"data": ""})
    assert response.status_code == 200
    assert "Could not read the data" in response.get_data(as_text=True)
