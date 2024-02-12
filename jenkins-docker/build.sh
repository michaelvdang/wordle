echo ===================Building the api===================
docker images
docker ps
docker ps -a
echo 'Creating new wordle-network...'
docker network create wordle-network

echo 'Creating new volume...'
docker volume create wordle-db

echo 'Build and run Redis container..'
docker build    -t redis-image ./app/services/Redis
docker run -d --volume wordle-db:/wordle/var --name redis -p 0.0.0.0:6379:6379 --network wordle-network redis-image
# docker run -d --name redis -p 0.0.0.0:6379:6379 --network wordle-network -v ./redis.conf:/data/redis.conf redis:alpine redis-server /data/redis.conf
# docker run -d --name redis -p 0.0.0.0:6379:6379 --network wordle-network -v ./redis.conf:/data/redis.conf redis:alpine redis-server /data/redis.conf

echo 'Build and run Stats container..'
docker build    -t stats-image ./app/services/Stats
docker run -d --volume wordle-db:/wordle/var --name stats -p 9000:9000 --network wordle-network stats-image

echo 'Build and run WordCheck container...'
docker build    -t wordcheck-image ./app/services/WordCheck
docker run -d --volume wordle-db:/wordle/var --name wordcheck -p 0.0.0.0:9100:9100 -h localhost --network wordle-network  wordcheck-image

echo 'Build and run WordValidation container...'
docker build    -t wordvalidation-image ./app/services/WordValidation
docker run -d --volume wordle-db:/wordle/var --name wordvalidation -p 0.0.0.0:9200:9200 -h localhost --network wordle-network wordvalidation-image

echo 'Build and run play container...'
docker build    -t play-image ./app/services/Play
docker run -d --name play -p 0.0.0.0:9300:9300 -h localhost --network wordle-network play-image

echo 'Build and run orc container...'
docker build    -t orc-image .
docker run -d --volume ./jenkins-docker/Deploy/:/wordle/jenkins-docker/Deploy/ --volume wordle-db:/wordle/var --name orc -p 9400:9400    --network wordle-network orc-image

# this might belong in the Test stage
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
