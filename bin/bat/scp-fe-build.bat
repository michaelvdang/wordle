@REM This script copies locally built frontend files to server at SERVER_IP
@REM set /p "USER=Enter user: "
@REM set /p "SERVER_IP=Enter SERVER_IP: "
@REM set /p "DOMAIN_NAME=Enter DOMAIN_NAME: "
set SERVER_IP=50.18.88.20
echo SERVER_IP: %SERVER_IP%
set DOMAIN_NAME=no-domain
echo DOMAIN_NAME: %DOMAIN_NAME%
set USER=ubuntu
echo USER: %USER%
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" -r ..\..\wordle-frontend\dist\* ubuntu@%SERVER_IP%:/home/%USER%/wordle/wordle-frontend/dist
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\..\wordle-frontend\dist\assets ubuntu@%SERVER_IP%:/home/ubuntu/%DOMAIN_NAME%
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\..\wordle-frontend\dist\* ubuntu@%SERVER_IP%:/var/www/%DOMAIN_NAME%/wordle
pause