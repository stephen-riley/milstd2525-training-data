# MIL-STD-2525 training dataset generator

This repository contains a dataset generator for MIL-STD-2525 training data.  It uses [milsymbol-py](https://github.com/stephen-riley/milsymbol-py) to generate PNGs of common MIL-STD-2525 symbols and a LLaVA JSON file for training Gemma 3 to identify the symbols. 

## Getting started

This repo uses `uv` for package management.  You must have `uv` installed to use this repo.

1. `git clone https://github.com/stephen-riley/milsymbol-py`
1. `git clone https://github.com/stephen-riley/milstd2525-training-data`
1. `cd milstd2525-training-data`
1. `uv venv`
1. `source .venv/bin/activate`
1. `uv pip install -e ../milsymbol-py`
1. `uv run gen_symbols.py`

This will generate `output/train.json` and `output/symbols/*png`.
