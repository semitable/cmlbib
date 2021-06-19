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

from cmlbib.binaries import load_aggregated_data

def update_entry(base, new, replace):
    new.pop('ID', None)
    base.update(new)

    if replace:
        for key in list(base.keys()):
            if key not in new and key != "ID":
                base.pop(key, None)


def cleanup_entries(db, abstract):
    for entry in db.entries:
        if not abstract:
            entry.pop("abstract", None)
    
    return db

@click.command()
@click.argument("input", type=click.Path(exists=True, dir_okay=False, writable=False))
@click.argument("output", type=click.Path(exists=False, dir_okay=False, writable=True, allow_dash=True))
@click.option("--replace/--no-replace", help="Fully replaces any matched bibliography entries.", default=True)
@click.option("--abstract/--no-abstract", help="Keeps or removes the abstract.", default=False)
def cli(input, output, replace, abstract):

    if Path(output).is_file():
        click.confirm("Output file already exists. Proceeding will OVERWRITE this file. Continue?", abort=True)

    db = load_aggregated_data()
    click.echo(f"Loaded full .bib data containing {len(db.entries)} entries")
    
    # load provided file
    with open(input, mode="r") as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        inputdb = bibtexparser.load(bibtex_file, parser=parser)
    click.echo(f"Loaded {input} containing {len(inputdb.entries)} entries")
    

    for entry in inputdb.entries:
        ltitle = " ".join(re.findall("[a-zA-Z]+", entry["title"])).lower()
        for dbentry in db.entries:
            db_title = " ".join(re.findall("[a-zA-Z]+", dbentry["title"])).lower()
            if ltitle == db_title:
                update_entry(entry, dbentry, replace)

    inputdb = cleanup_entries(inputdb, abstract)
        
    # print(inputdb.entries[0])
    writer = BibTexWriter()
    writer.indent = '    '
    with click.open_file(output, 'w') as bibfile:
        bibfile.write(writer.write(inputdb))



if __name__ == "__main__":
    cli()