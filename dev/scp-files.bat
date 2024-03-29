@REM This script copies files from windows computer to server at SERVER_IP
@REM set /p "USER=Enter user: "
@REM set /p "SERVER_IP=Enter SERVER_IP: "
set SERVER_IP=52.8.24.164
echo SERVER_IP: %SERVER_IP%
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\.env ubuntu@%SERVER_IP%:/home/ubuntu/wordle
scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\redis.conf ubuntu@%SERVER_IP%:/home/ubuntu/wordle/app/services/Redis/
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\wordle-frontend\.env ubuntu@%SERVER_IP%:/home/ubuntu/wordle/wordle-frontend

@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" server-init.sh ubuntu@%SERVER_IP%:/home/ubuntu/wordle/bin
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\crontab.txt ubuntu@%SERVER_IP%:/home/ubuntu/wordle
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\nginx-template.conf ubuntu@%SERVER_IP%:/home/ubuntu/wordle/nginx-template.conf
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\Orchestrator.py ubuntu@%SERVER_IP%:/home/ubuntu/wordle/Orchestrator.py
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\app\services\Stats\UserStatsRedis.py ubuntu@%SERVER_IP%:/home/ubuntu/wordle/app/services/Stats/UserStatRedis.py
@REM scp -i "C:\\Users\\Michael Dang\\.ssh\\kdgAWSKeyPair.pem" ..\wordle-frontend\src\component\* ubuntu@%SERVER_IP%:/home/ubuntu/wordle/wordle-frontend/src/component
pause