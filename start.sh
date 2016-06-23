#!/bin/bash

#set -e

PYTHON=python3

cd src

while : ; do
    $PYTHON scrape_test.py

    printf "\nCALCULATING ARBITRAGES\n"
    $PYTHON database_test.py

    printf "\nSLEEPING FOR 5 MINUTES\n"
    for i in $(seq 1 60); do
        sleep 10
        printf "."
    done

    printf "\n"
done
