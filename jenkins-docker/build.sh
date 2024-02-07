docker network create wordle-network
echo 'building Stats container..'
docker build    -t stats-image ./app/services/Stats
docker run -d --name stats -p 9000:9000 --network wordle-network stats-image

echo 'Building WordCheck container...'
docker build    -t wordcheck-image ./app/services/WordCheck
docker run -d --name wordcheck -p 9100:9100 -h localhost --network wordle-network  wordcheck-image

echo 'Building WordValidation container...'
docker build    -t wordvalidation-image ./app/services/WordValidation
docker run -d --name wordvalidation -p 9200:9200 -h localhost --network wordle-network wordvalidation-image

echo 'Building play container...'
docker build    -t play-image ./app/services/Play
docker run -d --name play -p 9300:9300 -h localhost --network wordle-network play-image

echo 'Building orc container...'
docker build    -t orc-image .
docker run -d --name orc -p 9400:9400    --network wordle-network orc-image

echo 'Buidling ubuntu-curler...'
docker build    -t ubuntu-image ./jenkins-docker/
docker run -d --name ubuntu-curler --network wordle-network ubuntu-image

docker logs orc
echo 'Containers in wordle-network:'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
