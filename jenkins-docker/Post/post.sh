echo Containers on wordle-network:
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
docker ps 
docker ps -a
docker images
docker images -f dangling=true
docker image prune -f
docker images
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
docker rmi -f wordle-connection-check-image
docker rmi -f wordle-api-tester-image

echo 'Stopping and removing the last container, image, and network'
docker stop wordle-connection-check
docker rm -f wordle-connection-check
docker stop wordle-api-tester
docker rm -f wordle-api-tester
docker network rm wordle-network
docker volume rm wordle-db
docker ps 
docker ps -a
docker images
rm .env
rm app/services/Redis/redis.conf