## to be run on a Linux Jenkins agent with docker installed
echo ===================Testing the api===================
# TopTen.py must run through a python container
echo Prepare Redis leaderboard:
docker exec orc python3 /wordle/bin/TopTen.py

# # API unit testing
# python -m pytest -vv
# # docker exec orc pytest -vv

# API integration testing
echo 'Buidling wordle-api-tester...'
whoami
mkdir -p logs
chmod o+w logs
ls -al
ls -al ./jenkins-docker
ls -al ./jenkins-docker/Test
ls -al ./jenkins-docker/Test/integration-api-test/
docker build   --progress plain -t wordle-api-tester-image ./jenkins-docker/Test/integration-api-test/
docker run -d --volume ./logs/:/data --name wordle-api-tester --network wordle-network wordle-api-tester-image

echo 'Check if container is on the network...'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network

echo 'Ping Redis...'
docker exec redis redis-cli -a "$REDIS_SECRET" ping
echo ''
echo 'Try to get keys from Redis...'
docker exec redis redis-cli -a "$REDIS_SECRET" keys *
echo ''
echo 'Ping Redis with wrong password'
docker exec redis redis-cli -a "hello" ping
echo ''
echo 'Ping Redis with no password'
docker exec redis redis-cli ping

rm -f after-test-docker-logs.txt
echo UTC date and time: `date +%m-%d\ %T` > logs/after-test-docker-logs.txt
# Redis logs
echo After-test logs from redis: >> logs/after-test-docker-logs.txt
docker logs redis >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Stats logs
echo After-test logs from stats: >> logs/after-test-docker-logs.txt
docker logs stats >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Check logs
echo After-test logs from check: >> logs/after-test-docker-logs.txt
docker logs check >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Validation logs
echo After-test logs from validation: >> logs/after-test-docker-logs.txt
docker logs validation >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Play logs
echo After-test logs from play: >> logs/after-test-docker-logs.txt
docker logs play >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
docker logs play
# Orc logs
echo After-test logs from orc: >> logs/after-test-docker-logs.txt
docker logs orc >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
docker logs orc


echo After-test logs from wordle-api-tester >> logs/after-test-docker-logs.txt
docker logs wordle-api-tester >> logs/after-test-docker-logs.txt
docker logs wordle-api-tester

# cat logs/after-test-docker-logs.txt
echo view logs in logs/after-test-docker-logs.txt