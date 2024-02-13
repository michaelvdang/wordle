#!/bin/bash
## run in the USER directory, ie. /home/$USER
whoami
date >> timestamp.txt

# check if repo has been cloned already, if yes stop containers and erase, then clone new repo
if [ -d wordle ]
then 
  cd wordle
  docker compose down
  cd 
  sudo rm -rf wordle
fi

git clone https://github.com/michaelvdang/wordle.git
cd wordle
git checkout docker-jenkins
