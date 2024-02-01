@REM set /p "USER=Enter user: "
set /p "SERVER_IP=Enter SERVER_IP: "
echo SERVER_IP: %SERVER_IP%
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\.env ubuntu@%SERVER_IP%:/home/ubuntu/wordle
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\redis.conf ubuntu@%SERVER_IP%:/home/ubuntu/wordle
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" .\server-init.sh ubuntu@%SERVER_IP%:/home/ubuntu/wordle/bin
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\crontab.txt ubuntu@%SERVER_IP%:/home/ubuntu/wordle
pause