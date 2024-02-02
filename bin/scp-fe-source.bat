set SERVER_IP=50.18.88.20
echo SERVER_IP: %SERVER_IP%
set USER=ubuntu
echo USER: %USER%
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" -r ..\wordle-frontend\src\* ubuntu@%SERVER_IP%:/home/%USER%/wordle/wordle-frontend/src
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" -r ..\wordle-frontend\.env ubuntu@%SERVER_IP%:/home/%USER%/wordle/wordle-frontend/.env
