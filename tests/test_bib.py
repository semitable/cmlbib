import os
import sys
import pytest
import re
import string

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding, convert_to_unicode
from pathlib import Path
import pprint

_stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


_pp = pprint.PrettyPrinter(indent=4)
_bibs = list(Path("data/").glob('**/*.bib'))

_bib_data = []

for fname in _bibs:
    with open(fname, 'r') as handle:
        _parser = BibTexParser(common_strings=False)
        _parser.customization = convert_to_unicode
        _bib_data.append(bibtexparser.load(handle, parser=_parser))

@pytest.mark.parametrize("db", _bib_data, ids=[b.stem for b in _bibs])
def test_title(db):
    for entry in db.entries:
        assert "title" in entry, f"No title in entry with id: {entry['ID']}"
        assert len(entry["title"]) > 1,  f"Title too short (<=1 character) in entry with id: {entry['ID']}"
        # assert entry["title"].istitle(), f"Title not properly capitalised in entry with id {entry['ID']}"

@pytest.mark.parametrize("db", _bib_data, ids=[b.stem for b in _bibs])
def test_pages(db):
    for entry in db.entries:
        assert "pages" in entry, f"No pages in entry with id: {entry['ID']}"
        assert "--" in entry["pages"], f"No page range (e.g. --) found in entry with id: {entry['ID']}"
        assert re.match(r"^[0-9]+--[0-9]+$", entry["pages"]), f"Page range not in XX--XX form in entry with id: {entry['ID']}"

