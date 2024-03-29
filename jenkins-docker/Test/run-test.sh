## to be run on a Linux Jenkins agent with docker installed
echo ===================Testing the api===================
# TopTen.py must run through a python container
docker exec orc python3 /wordle/bin/TopTen.py

echo 'Build and run wordle-connection-check...'
docker build    -t wordle-connection-check-image ./jenkins-docker/ConnectionCheck/
docker run -d --name wordle-connection-check --network wordle-network wordle-connection-check-image

echo 'Log from orc container: '
docker logs orc
echo 'Connection status between wordle-connection-check and other containers:'
docker logs wordle-connection-check
echo ''
echo 'Containers in wordle-network:'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network


echo 'Buidling wordle-api-tester...'
docker build    -t wordle-api-tester-image ./jenkins-docker/Test
docker run -d --volume ./logs/:/data --name wordle-api-tester --network wordle-network wordle-api-tester-image

echo 'Check if container is on the network...'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network

echo 'Ping Redis...'
docker exec redis redis-cli -a "$REDIS_SECRET" ping


touch after-test-logs.txt
echo After-test logs from redis: >> after-test-logs.txt
docker logs redis >> after-test-logs.txt
echo After-test logs from stats: >> after-test-logs.txt
docker logs stats >> after-test-logs.txt
echo After-test logs from wordcheck: >> after-test-logs.txt
docker logs wordcheck >> after-test-logs.txt
echo After-test logs from wordvalidation: >> after-test-logs.txt
docker logs wordvalidation >> after-test-logs.txt
echo After-test logs from play: >> after-test-logs.txt
docker logs play >> after-test-logs.txt
echo After-test logs from orc: >> after-test-logs.txt
docker logs orc >> after-test-logs.txt


echo After-test logs from wordle-api-tester >> after-test-logs.txt
docker logs wordle-api-tester >> after-test-logs.txt

# cat after-test-logs.txt
echo view logs in after-test-logs.txt