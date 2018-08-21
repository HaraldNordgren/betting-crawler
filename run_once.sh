#!/bin/bash

set -e
PYTHON=python3

function require {
    cmd=$1
    command -v "$cmd" > /dev/null 2>&1 || {
        echo >&2 "I require '$cmd' but it's not installed. Aborting."
        exit 1
    }
}
require scrapy
require $PYTHON

function python_require {
    package=$1
    if ! $PYTHON -m pip show "$package" 1> /dev/null; then
        echo >&2 "I require python package '$package' but it's not installed."
        exit 1
    fi
}
python_require scrapy

if [[ -n "$DYNO" ]]; then
    echo "On Heroku"
fi
cd src

scrapy runspider betway_scrapy.py 
#$PYTHON scrape_test.py

printf "\nCALCULATING ARBITRAGES\n"
$PYTHON database_test.py
printf "\n"

