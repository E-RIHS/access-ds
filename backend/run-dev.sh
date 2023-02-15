#!/usr/bin/env bash

cd "$(dirname "$0")"

# create the virtual environment (if it doesn't already exists)
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# activate the virtual environment
source . ../venv/bin/activate

# install (or update) the dependencies
pip install -r requirements.txt

# get schemas and configurations from Github
cd src
python get_schemas.py

# and finally, run the application using the Uvicorn web server:
uvicorn main:app --reload
