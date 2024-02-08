echo ===================Testing the api===================
echo 'Buidling wordle-api-tester...'
docker build    -t wordle-api-tester-image ./jenkins-docker/Test
docker run -d --name wordle-api-tester --network wordle-network wordle-api-tester-image

echo 'Check if container is on the network...'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
