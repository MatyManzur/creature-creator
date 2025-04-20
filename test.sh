#!/bin/bash
source .venv/bin/activate
export PYHTONPATH=src
python -m unittest discover -s tests -p "*.py"
deactivate