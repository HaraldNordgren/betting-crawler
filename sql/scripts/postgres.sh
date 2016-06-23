#!/bin/bash

#self.connection = psycopg2.connect(host='ec2-54-83-198-111.compute-1.amazonaws.com', user='pjormmuewnnkwm', password='tf5q17_nrEOswfolbd3PS6wmNF', dbname='da3j6ejvc5arr0', port=5432)

export PGPASSWORD='tf5q17_nrEOswfolbd3PS6wmNF'
psql -U 'pjormmuewnnkwm' -h 'ec2-54-83-198-111.compute-1.amazonaws.com' -d 'da3j6ejvc5arr0' -p 5432
