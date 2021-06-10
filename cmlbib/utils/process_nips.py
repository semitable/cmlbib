import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding, convert_to_unicode

from pathlib import Path
import json
import click
import pickle
import re
from match import match_titles
from tqdm import tqdm

def normalize_title(title_str):
    title_str = re.sub(r'[^a-zA-Z]',r'', title_str) 
    return title_str.lower().strip()
    # return title_str.lower().replace(" ", "").strip()

bibs = Path("../../raw/dblp/").glob('*.bib')
# strdb = ""
# for fname in ["../../tmp/neurips2020.bib"]:
parser = BibTexParser(common_strings=False)
parser.customization = convert_to_unicode
# neurips = bibtexparser.load(file, parser=parser)
prev_loaded = 0
for fname in sorted(bibs):
    with open(fname, 'r') as handle:
        # strdb += infile.read()
        dblp = bibtexparser.load(handle, parser=parser)
    print(f"Loaded {len(dblp.entries) - prev_loaded} entries from {fname}")
    prev_loaded = len(dblp.entries)
click.echo(f"Loaded full raw/dblp/*.bib data containing {len(dblp.entries)} entries")


with open('../../raw/proceedings/neurips.bib', 'r') as file:
    parser = BibTexParser(common_strings=False)
    parser.customization = convert_to_unicode
    neurips = bibtexparser.load(file, parser=parser)
click.echo(f"Loaded full raw/proceedings/neurips.bib data containing {len(neurips.entries)} entries")

# parser = BibTexParser(common_strings=True)
# parser.customization = convert_to_unicode
# dblp = bibtexparser.loads(strdb, parser=parser)
# click.echo(f"Loaded full neurips2020.bib data containing {len(dblp.entries)} entries")
# with open("../../tmp/dblp.p", "wb") as file:
#     pickle.dump(dblp, file, protocol=pickle.HIGHEST_PROTOCOL)

# with open('../../tmp/neurips.p', 'rb') as handle:
#     neurips = pickle.load(handle)
# click.echo(f"Loaded full neurips.bib data containing {len(neurips.entries)} entries")
# with open('../../raw/proceedings/neurips.bib', 'r') as file:
#     parser = BibTexParser(common_strings=False)
#     parser.customization = convert_to_unicode
#     neurips = bibtexparser.load(file, parser=parser)
# click.echo(f"Loaded full neurips.bib data containing {len(neurips.entries)} entries")
# with open('../../tmp/dblp.p', 'rb') as handle:
#     dblp = pickle.load(handle)
# click.echo(f"Loaded full dblp.bib data containing {len(dblp.entries)} entries")

years = set([entry["year"] for entry in neurips.entries] + ["1987"])
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

dblp.entries = [entry for entry in dblp.entries if "nips" in entry["ID"]]

for year in sorted(years)[::-1]:
    filename = f"../../data/nips/nips{year}.bib"
    writer = BibTexWriter()
    writer.indent = '    '
    new_db = BibDatabase()
    # something is wrong with the years in up to ~2009-2010. ID appears to be correct
    new_db.entries = [entry for entry in neurips.entries if entry["ID"].startswith(f"NIPS{year}") or entry["ID"].startswith(f"NEURIPS{year}")]
    for entry in new_db.entries:
        entry["year"] = year
    
    updates = []
    for entry in tqdm(new_db.entries):
        # norm_title = entry["title"].replace("\textquote", "")
        # norm_title = entry["title"].replace("\textbackslash", "")
        if "&amp;" in entry["title"]:
            entry["title"] = entry["title"].replace("&amp;", "&")
        title_a = normalize_title(entry["title"])
        
        for dblp_entry in dblp.entries:
            title_b = normalize_title(dblp_entry["title"])

            if title_a[:3] == title_b[:3] and (title_a.replace(" ", "") == title_b.replace(" ", "") or match_titles(title_a, title_b)):
                if "pages" not in entry or entry["pages"] == "":
                    entry["pages"] = dblp_entry.get("pages", "")
                if "editor" in dblp_entry:
                    entry["editor"] = " ".join(dblp_entry["editor"].split())

                address = dblp_entry["booktitle"].split(", ")[-2:]

                if address[-1].lower() == "virtual" or address[-1].lower() == "online":
                    address = "Online"
                else:
                    address = ", ".join(address)

                entry["address"] = address
                try:
                    entry["month"] = [str(i+1) for i in range(len(months)) if months[i] in dblp_entry["booktitle"]][0]
                except:
                    pass

                updates.append(1.0)
                break
        else:
            tqdm.write(f"Could not find: {entry['title']} - {title_a}")
            updates.append(0)
    
    tqdm.write(f"Updated {sum(updates)/len(updates)*100:.1f}% of values")
    
    tqdm.write(f"Creating {filename}")
    with open(filename, 'w') as bibfile:
        bibfile.write(writer.write(new_db))

