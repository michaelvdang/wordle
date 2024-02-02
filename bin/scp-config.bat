@REM set /p "USER=Enter user: "
@REM set /p "SERVER_IP=Enter SERVER_IP: "
set SERVER_IP=50.18.88.20
echo SERVER_IP: %SERVER_IP%
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\.env ubuntu@%SERVER_IP%:/home/ubuntu/wordle
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\redis.conf ubuntu@%SERVER_IP%:/home/ubuntu/wordle
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" .\server-init.sh ubuntu@%SERVER_IP%:/home/ubuntu/wordle/bin
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\crontab.txt ubuntu@%SERVER_IP%:/home/ubuntu/wordle
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\nginx-template.conf ubuntu@%SERVER_IP%:/home/ubuntu/wordle/nginx-template.conf
pause