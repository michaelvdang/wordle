#!/bin/bash
## run in the USER directory, ie. /home/$USER
whoami
date >> timestamp.txt

# check if repo has been cloned already, if yes stop containers and erase, then clone new repo
if [ -d wordle ]
then 
  ls -al
  cd wordle
  docker compose down
  cd 
  sudo rm -rf wordle
  ls -al
  docker rmi wordle-orc wordle-stats wordle-check wordle-validation wordle-play
fi

git clone https://github.com/michaelvdang/wordle.git
cd wordle
git checkout testing
