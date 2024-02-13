#!/bin/bash
whoami
date >> timestamp.txt
git clone https://github.com/michaelvdang/wordle.git
cd wordle
git pull
git checkout docker-jenkins

# chmod +x ./bin/server-init.sh
