Introduction
============

Betting Crawler is a program for extracting football odds from various sports betting sites and match them against each other to find arbitrages. An arbitrage is a situation where each of the three options 1, X and 2 give such a high return that placing a bet on each one gives a guaranteed profit.

The program currently scrapes Betway, Nordicbet, Nordicbet.


Running the program
===================

The program has a number of dependencies. Assuming you are running Ubuntu, run the following to install packages:

```
sudo apt-get install python3 python3-pip postgresql libpq-dev

sudo pip3 install splinter psycopg2
```


Then run `./src/scrape_test.py` to scrape websites. All the odds data is stored in a database and can be accessed anytime. Re-running the scaper will update the old odds and tell you have has been changed.

Running `./src/database_test.py` corroborates all the data in the DB to find arbitrages.
