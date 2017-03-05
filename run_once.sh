#!/bin/bash

set -e

if [[ -n "$DYNO" ]]; then
    echo "On Heroku"
fi

cd src
PYTHON=python3

scrapy runspider betway_scrapy.py 
$PYTHON scrape_test.py

printf "\nCALCULATING ARBITRAGES\n"
$PYTHON database_test.py

printf "\n"
