#!/bin/sh
# this script is for running in containers
mkdir -p /wordle/var
# sqlite3 /wordle/var/WordList.db < /wordle/share/WordList.sql
# sqlite3 /wordle/var/Answers.db < /wordle/share/Answers.sql
python3 /wordle/bin/wordlist.py
python3 /wordle/bin/answers.py
python3 /wordle/bin/stats.py
python3 /wordle/bin/shard.py
