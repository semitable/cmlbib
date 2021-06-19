from setuptools import setup

setup(
    name='cmlbib',
    version='0.1.0',
    py_modules=['cmlbib'],
    install_requires=[
        'Click==8.*',
        'bibtexparser==1.2.0',
        'tqdm==4.*'
    ],
    entry_points={
        'console_scripts': [
            'cmlbib-sanitize = cmlbib:cli',
            'cmlbib-export = cmlbib:export',
        ],
    },
)