## to be run on a Linux Jenkins agent with docker installed
echo ===================Testing the api===================
echo 'Buidling wordle-api-tester...'
docker build    -t wordle-api-tester-image ./jenkins-docker/Test
docker run -d --volume wordle-db:/data --volume ./:/data --name wordle-api-tester --network wordle-network wordle-api-tester-image

echo 'Check if container is on the network...'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network

echo 'Ping Redis...'
# docker exec redis redis-cli ping
docker exec redis redis-cli -a $REDIS_SECRET ping


sh 'sleep 5'
echo 'After test logs from wordvalidation:'
sh 'docker logs wordvalidation'
echo 'After test logs from play:'
sh 'docker logs play'
echo 'After test logs from orc:'
sh 'docker logs orc'
sh '''
  echo ''
  echo 'Log from wordle-api-tester'
  docker logs wordle-api-tester
  echo ''
'''