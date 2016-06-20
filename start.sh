#!/bin/bash

PYTHON=python3

cd src

while : ; do
    $PYTHON scrape_test.py

    echo; echo "CALCULATING ARBITRAGES:"
    $PYTHON database_test.py

    echo "SLEEPING FOR 5 MINUTES"
    for i in $(seq 1 60); do
        sleep 10
        echo -n "."
    done
done
