#!/bin/sh
mkdir -p ./var
sqlite3 ./var/WordList.db < ./share/WordList.sql
sqlite3 ./var/Answers.db < ./share/Answers.sql

