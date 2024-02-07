echo 'Buidling wordle-api-tester...'
docker build    -t wordle-api-tester-image ./jenkins-docker/Test
docker run -d --name wordle-api-tester --network wordle-network wordle-api-tester-image
