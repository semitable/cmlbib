import json
import re
import click
import bibtexparser
from tqdm import tqdm
from pathlib import Path

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding, convert_to_unicode

def load_bib_data():

    path = Path(__file__).parents[1] / "data"
    bibs = list(path.glob('**/*.bib'))
    parser = BibTexParser(common_strings=False)
    parser.customization = convert_to_unicode

    for fname in tqdm(bibs):
        with click.open_file(fname, 'r') as handle:
            bib_data = bibtexparser.load(handle, parser=parser)
    
    return bib_data


def export_to_json(bib, path):
    with open(path, 'w') as outfile:
        json.dump(bib.entries, outfile)

def import_from_json(path):
    with open(path, 'r') as json_file:
        entries = json.load(json_file)

    db = BibDatabase()
    db.entries = entries
    return db


@click.group()
def cli():
    pass

@cli.command()
@click.argument("output", type=click.Path(exists=False, dir_okay=False, writable=True, allow_dash=True), default=Path(__file__).parents[1] / "build" / "aggregate.json")
def export(output):

    Path(output).parent.mkdir(exist_ok=True, parents=True)

    db = load_bib_data()
    export_to_json(db, output)

if __name__ == "__main__":
    cli()
