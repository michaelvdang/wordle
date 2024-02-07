docker network inspect {{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network
docker ps 
docker ps -a
docker images
docker images -f dangling=true
docker image prune -f
docker images
docker stop stats
docker stop wordcheck
docker stop wordvalidation
docker stop play
docker stop orc
docker stop ubuntu-tester
docker network rm wordle-network
docker ps 
docker ps -a