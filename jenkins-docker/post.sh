echo Containers on wordle-network:
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
docker ps 
docker ps -a
docker images
docker images -f dangling=true
docker image prune -f
docker images

echo "Debugging Redis START"
docker logs redis
echo "END debugging Redis"

echo Stopping the following containers: 
docker stop redis
docker stop stats
docker stop wordcheck
docker stop wordvalidation
docker stop play
docker stop orc
echo Removing containers:
docker rm -f redis
docker rm -f stats
docker rm -f wordcheck
docker rm -f wordvalidation
docker rm -f play
docker rm -f orc
echo Removing images
docker rmi -f redis-image
docker rmi -f stats-image
docker rmi -f wordcheck-image
docker rmi -f wordvalidation-image
docker rmi -f play-image
docker rmi -f orc-image
docker rmi -f wordle-status-check-image
docker rmi -f wordle-api-tester-image
echo ''
echo 'Log from wordle-status-check'
docker logs wordle-status-check
echo ''
echo ''
echo 'Log from wordle-api-tester'
docker logs wordle-api-tester
echo ''
echo 'Stopping and removing the last container, image, and network'
docker stop wordle-status-check
docker rm -f wordle-status-check
docker stop wordle-api-tester
docker rm -f wordle-api-tester
docker network rm wordle-network
docker ps 
docker ps -a
docker images
rm .env
rm app/services/Redis/redis.conf