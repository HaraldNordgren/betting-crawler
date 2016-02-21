#!/bin/bash

export PGPASSWORD=admin
psql -U postgres -h localhost -d odds_data
