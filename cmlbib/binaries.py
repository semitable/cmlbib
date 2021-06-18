import json
import click
import bibtexparser
from tqdm import tqdm
import gzip
from pathlib import Path
import shutil
import urllib.request
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


def export_to_file(bib, path):
    with gzip.open(path.with_suffix(".gz"), 'wb') as fout:
        fout.write(json.dumps(bib.entries).encode("utf-8"))

def unzip_file(path):
    click.echo(f"Decompressing data to {path}")

    with gzip.open(path.with_suffix(".gz"), 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))
    with open(path, "w") as fout:
        json.dump(data, fout)


def load_aggregated_data(path = Path(__file__).absolute().parents[1] / "build" / "aggregate.json", overwrite_latest = False):

    Path(path).parent.mkdir(exist_ok=True, parents=True)

    if overwrite_latest or (not path.exists() and not path.with_suffix(".gz").exists()):
        download_latest()

    if overwrite_latest or (not path.exists() and (path.with_suffix(".gz")).exists()):
        unzip_file(path)

    if path.exists():
        with open(path, 'r') as fin:
            entries = json.load(fin)
        db = BibDatabase()
        db.entries = entries
        return db
    else:
        raise FileNotFoundError()

def download_latest():
    url = "https://github.com/semitable/cmlbib/releases/latest/download/aggregate.gz"
    path = Path(__file__).absolute().parents[1] / "build" / "aggregate.gz"
    
    click.echo(f"Downloading compressed bib data from {url}")
    
    with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


@click.group()
def cli():
    pass

@cli.command()
@click.argument("output", type=click.Path(exists=False, dir_okay=False, writable=True, allow_dash=True), default=Path(__file__).absolute().parents[1] / "build" / "aggregate.json")
def export(output):

    Path(output).parent.mkdir(exist_ok=True, parents=True)

    db = load_bib_data()
    export_to_file(db, output)


if __name__ == "__main__":
    cli()
