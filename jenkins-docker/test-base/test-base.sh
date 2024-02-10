# testing fastapi
docker ps
docker ps -a
docker images
docker build -t fa-image ./app/services/base
docker run -d --name fa-cont --network wordle-network fa-image
docker build -t fa-tester-image ./jenkins-docker/test-base
docker run -d --name fa-tester --network wordle-network fa-tester-image
docker logs fa-tester
docker logs fa-cont

docker rm -f fa-cont
docker rmi -f fa-image
docker rm -f fa-tester
docker rmi -f fa-tester-image