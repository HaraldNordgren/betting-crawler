#!/bin/bash

while : ; do
    python3 src/scrape_test.py
    python3 src/database_test.py > hello/templates/index.html
    sleep 600
done
