#!/bin/sh 
# this script is for running directly in bash (not containers)
rm -r var
mkdir -p ./var
sqlite3 ./var/WordList.db < ./share/WordList.sql
sqlite3 ./var/Answers.db < ./share/Answers.sql

python3 bin/stats.py
python3 bin/shard.py