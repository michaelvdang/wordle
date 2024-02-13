#!/bin/bash
#### Run this script in an EC2 Ubuntu instance from the project root
####  this will install the entire application that can be accessed at
####  SERVER_IP of the EC2 instance. You'll need to get a domain name
####  and point DNS to SERVER_IP, if needed, run certbot
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

# ## copy credentials files with scp-secret.bat on windows
# until [ -f ./.env ]
# do
#   echo .env is missing from project_root. Run scp-secret.bat to copy the files containing passwords
#   sleep 10
# done
# echo .env found
# until [ -f ./app/services/Redis/redis.conf ]
# do 
#   echo redis.conf is missing from project_root/app/services/Redis/ Run scp-secret.bat to copy the files containing passwords
#   sleep 10
# done
# echo redis.conf found in project_root/app/services/Redis/

## run crontab
sudo crontab /home/${USER}/wordle/crontab.txt

## install pip, venv, and requirements for crontab
sudo apt -y install python3-pip
sudo python3 -m pip install -r cron-requirements.txt

## start the services
sudo docker compose up -d

## install NGINX
sudo apt update
sudo apt -y install nginx

sudo ufw allow 'Nginx HTTP'
# extras
echo ufw status:
sudo ufw status

curl -4 icanhazip.com
# end extras

## configure NGINX
  # get env variables, including: DOMAIN_NAME
source .env

  # remove carriage return from $SERVER_IP
SERVER_IP=`echo $SERVER_IP | tr -d "\r" | cat -v`
DOMAIN_NAME=`echo $DOMAIN_NAME | tr -d "\r" | cat -v`
VITE_DOMAIN_NAME=`echo $VITE_DOMAIN_NAME | tr -d "\r" | cat -v`
VITE_BACK_END_TYPE=`echo $VITE_BACK_END_TYPE | tr -d "\r" | cat -v`

  # create frontend .env file
echo $VITE_DOMAIN_NAME > /home/${USER}/wordle/wordle-frontend/.env
echo $VITE_BACK_END_TYPE >> /home/${USER}/wordle/wordle-frontend/.env

  # copy template to new file
sudo cat nginx-template.conf > $DOMAIN_NAME.conf
  # replace <SERVER_IP> in config file with SERVER_IP from .env
sed -i "s/<SERVER_IP>/$SERVER_IP/g" $DOMAIN_NAME.conf
sed -i "s/<DOMAIN_NAME>/$DOMAIN_NAME/g" $DOMAIN_NAME.conf
  # move config file and create soft link
sudo mv $DOMAIN_NAME.conf /etc/nginx/sites-available
  # remove old links
sudo rm /etc/nginx/sites-enabled/$DOMAIN_NAME
sudo ln -s /etc/nginx/sites-available/$DOMAIN_NAME.conf /etc/nginx/sites-enabled/$DOMAIN_NAME

sudo nginx -s reload

## make NGINX static files directory
sudo mkdir -p /var/www/$DOMAIN_NAME
sudo mkdir -p /var/www/$DOMAIN_NAME/wordle

## METHOD 1: build the app ON server
cd /home/$USER/wordle/wordle-frontend
## installing node and npm
# fix broken install 
  # sudo rm /etc/apt/sources.list
  # sudo apt --fix-broken install
  # sudo apt update
  # sudo apt remove nodejs
  # sudo apt remove nodejs-doc
# end fix
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y curl
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nodejs_20.11.0-1nodesource1_amd64.deb
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y
sudo apt -y install npm 
npm i
npm run build

# ## METHOD 2: build app LOCALLY
# read -p "Before movign on, if we are not building the app on server, make sure to run scp-fe-build.bat with the correct SERVER_IP to copy html assets to server. Press ENTER to continue..."
# sudo mkdir -p /home/$USER/wordle/wordle-frontend/dist

sudo cp -r /home/$USER/wordle/wordle-frontend/dist/* /var/www/$DOMAIN_NAME/wordle/

echo App can now be accessed at $IP_ADDRESS/wordle
sleep 10