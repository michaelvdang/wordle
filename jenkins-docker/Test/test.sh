## to be run on a Linux Jenkins agent with docker installed
echo ===================Testing the api===================
echo 'Buidling wordle-api-tester...'
docker build    -t wordle-api-tester-image ./jenkins-docker/Test
docker run -d --volume ./logs/:/data --name wordle-api-tester --network wordle-network wordle-api-tester-image

echo 'Check if container is on the network...'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network

echo 'Ping Redis...'
# docker exec redis redis-cli ping
docker exec redis redis-cli -a $REDIS_SECRET ping


sleep 5
# pwd
# ls -al
echo After-test logs from stats:
docker logs stats > a-stats-log.txt
echo After-test logs from wordcheck:
docker logs wordcheck > a-wc-log.txt
echo After-test logs from wordvalidation:
docker logs wordvalidation > awv-log.txt
echo After-test logs from play:
docker logs play > aplay-log.txt
echo After-test logs from orc:
docker logs orc > aorc-log.txt
echo After-test logs from redis:
docker logs redis > a-redis-log.txt

echo 'Log from wordle-api-tester'
docker logs wordle-api-tester > a-tester-log.txt
cat a-tester-log.txt
