#!/bin/bash
### Backend
## installing Docker
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# Add Docker's official GPG key:
sudo apt-get -y update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# fix permission denied for docker
sudo groupadd -f docker
sudo usermod -aG docker ${USER}
sudo service docker restart

### Frontend, when you want to build the front end on the server
## installing npm
sudo apt -y install npm 

## copy credentials files with scp-secret.bat on windows
until [ -f ./.env ]
do
  echo .env is missing. Run scp-secret.bat to copy the files containing passwords
  sleep 10
done
echo .env found
until [ -f ./redis.conf ]
do 
  echo redis.conf is missing. Run scp-secret.bat to copy the files containing passwords
  sleep 10
done
echo redis.conf found

## run crontab
sudo crontab /home/${USER}/wordle/crontab.txt

## install pip, venv, and requirements for crontab
sudo apt -y install python3-pip
sudo python3 -m pip install -r cron-requirements.txt

## start the services
sudo docker compose up -d