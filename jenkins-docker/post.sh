echo Containers on wordle-network:
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
docker ps 
docker ps -a
docker images
docker images -f dangling=true
docker image prune -f
docker images
echo Stopping the following containers: 
docker stop stats
docker stop wordcheck
docker stop wordvalidation
docker stop play
docker stop orc
echo Removing containers:
docker rm -f stats
docker rm -f wordcheck
docker rm -f wordvalidation
docker rm -f play
docker rm -f orc
echo Removing images
docker rmi -f stats-image
docker rmi -f wordcheck-image
docker rmi -f wordvalidation-image
docker rmi -f play-image
docker rmi -f orc-image
docker rmi -f ubuntu-image 095e68df905a

echo -e \nLog from ubuntu-tester\n
docker logs ubuntu-tester
docker stop ubuntu-tester
docker rm -f ubuntu-tester
docker network rm wordle-network
docker ps 
docker ps -a