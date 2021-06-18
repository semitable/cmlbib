from setuptools import setup

setup(
    name='cmlbib',
    version='0.1.0',
    py_modules=['cmlbib'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cmlbib-sanitize = cmlbib:cli',
            'cmlbib-export = cmlbib:export',
        ],
    },
)