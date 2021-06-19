# CMLBIB: Curated ML .bib for LaTeX

Is your bibliography inconsistent? Does it include the year or month in one entry but not in others? Are some entries all-caps and others in Title Case? ... Does it list enties as ArXiv pre-preprints while they are published in conferences?

CMLBIB attempts to solve this by 
1. maintaining curated .bib entries for papers in top ML conferences 
2. providing a tool that automatically matches your .bib entries to ours and fixing them for you.

# Installation

CMLBIB uses Python 3 and is in PyPI. You can install it using
```sh
pip install cmlbib
```

You can also install it from this repository:
```sh
git clone git@github.com:semitable/cmlbib.git
cd cmlbib
pip install -e .
```

# Usage
Installing CMLBIB adds `cmlbib-sanitize` to your command lines.

For an example of its usage using the default settings see below. This will export an output.bib file where some entries (any bibliography entries that have been matched to our curated bibliography) have been replaced.
```sh
cmlbib-sanitize example.bib output.bib
```

For help use:
```sh
cmlbib-sanitize --help
```

# An Opinionated Collection of .bib Files
The `data/` folder contains the collection of .bib files from several conferences.
Ideally we would like each entry to resemble:
```tex
@inproceedings{NEURIPS2020_7967cc8e, % ID not important, as long as its unique.
    address = {Online}, % or perhaps {Lille, France}. Do not include dates or anything else.
    author = {Christianos, Filippos and Schäfer, Lukas and Albrecht, Stefano}, % Note unicode encoding
    booktitle = {Advances in Neural Information Processing Systems}, % If in original conference name, "Proceedings of.." should be included. Do not include dates/locations or abbraviations here.
    editor = {Hugo Larochelle and Marc'Aurelio Ranzato and Raia Hadsell and Maria-Florina Balcan and Hsuan-Tien Lin},
    month = {12}, % month in numeric format: 1..12
    pages = {10707--10717}, % pages should be inluded
    publisher = {Curran Associates, Inc.},
    title = {Shared Experience Actor-Critic for Multi-Agent Reinforcement Learning}, % note Title Case
    volume = {33}, % Always include if it exists
    year = {2020} % Always include
}
```

# Contributing
We welcome contributions, especially new conferences and .bib files. Add files to the respective folders under `data/` and make a pull request.

**However** - CMLBIB prefers not having an entry to having it *wrong*. Prefer collecting data from the Proceedings (e.g. http://proceedings.mlr.press/v119/ - click first bib link) and make a reasonable attempt at curating it by making sure entries are similar to the above. You can also use DBLP *but* make sure to clear it up since it tends to add addresses/dates to the booktitle entry.

You can run the included tests to check they are similar to the above using `pytest`.


