docker images
docker ps
docker ps -a
echo 'Creaeting new wordle-network...'
docker network create wordle-network

echo 'Build and run Redis container..'
docker run -d --name redis -p 0.0.0.0:6379:6379 --network wordle-network -v ./redis.conf:./redis.conf redis:alpine redis-server /redis.conf

echo 'Build and run Stats container..'
docker build    -t stats-image ./app/services/Stats
docker run -d --name stats -p 9000:9000 --network wordle-network stats-image

echo 'Build and run WordCheck container...'
docker build    -t wordcheck-image ./app/services/WordCheck
docker run -d --name wordcheck -p 0.0.0.0:9100:9100 -h localhost --network wordle-network  wordcheck-image

echo 'Build and run WordValidation container...'
docker build    -t wordvalidation-image ./app/services/WordValidation
docker run -d --name wordvalidation -p 0.0.0.0:9200:9200 -h localhost --network wordle-network wordvalidation-image

echo 'Build and run play container...'
docker build    -t play-image ./app/services/Play
docker run -d --name play -p 0.0.0.0:9300:9300 -h localhost --network wordle-network play-image

echo 'Build and run orc container...'
docker build    -t orc-image .
docker run -d --name orc -p 9400:9400    --network wordle-network orc-image

echo 'Build and run wordle-status-check...'
docker build    -t wordle-status-check-image ./jenkins-docker/
docker run -d --name wordle-status-check --network wordle-network wordle-status-check-image


echo 'Log from orc container: '
docker logs orc
echo 'Containers in wordle-network:'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
