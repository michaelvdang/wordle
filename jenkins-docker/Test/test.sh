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
chmod u+x -R ./logs
echo After-test logs from wordvalidation:
docker logs wordvalidation > ./logs/wv-log.txt
echo After-test logs from play:
docker logs play > ./logs/play-log.txt
echo After-test logs from orc:
docker logs orc > ./logs/orc-log.txt

echo 'Log from wordle-api-tester'
docker logs wordle-api-tester
