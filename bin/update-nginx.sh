## WORKDIR project_root
## configure NGINX
  # get env variables, including: DOMAIN_NAME
source .env

  # remove carriage return from $VITE_SERVER_IP
VITE_SERVER_IP=`echo $VITE_SERVER_IP | tr -d "\r" | cat -v`
# DOMAIN_NAME=`echo $DOMAIN_NAME | tr -d "\r" | cat -v`
VITE_DOMAIN_NAME=`echo $VITE_DOMAIN_NAME | tr -d "\r" | cat -v`
VITE_BACK_END_TYPE=`echo $VITE_BACK_END_TYPE | tr -d "\r" | cat -v`

  # copy template to new file
sudo cat nginx-template.conf > $VITE_DOMAIN_NAME.conf
  # replace <VITE_SERVER_IP> in config file with VITE_SERVER_IP from .env
sed -i "s/<VITE_SERVER_IP>/$VITE_SERVER_IP/g" $VITE_DOMAIN_NAME.conf
sed -i "s/<DOMAIN_NAME>/$VITE_DOMAIN_NAME/g" $VITE_DOMAIN_NAME.conf
  # move config file and create soft link
sudo mv $VITE_DOMAIN_NAME.conf /etc/nginx/sites-available
  # remove old links
sudo rm /etc/nginx/sites-enabled/$VITE_DOMAIN_NAME
sudo ln -s /etc/nginx/sites-available/$VITE_DOMAIN_NAME.conf /etc/nginx/sites-enabled/$VITE_DOMAIN_NAME




