echo 'Check if container is on the network...'
docker network inspect --format='{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}' wordle-network

echo UTC date and time: `date +%m-%d\ %T` > logs/after-test-docker-logs.txt
# Redis logs
echo After-test logs from redis: >> logs/after-test-docker-logs.txt
docker logs redis >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Stats logs
echo After-test logs from stats: >> logs/after-test-docker-logs.txt
docker logs stats >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Check logs
echo After-test logs from check: >> logs/after-test-docker-logs.txt
docker logs check >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Validation logs
echo After-test logs from validation: >> logs/after-test-docker-logs.txt
docker logs validation >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
# Play logs
echo After-test logs from play: >> logs/after-test-docker-logs.txt
docker logs play >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
docker logs play
# Orc logs
echo After-test logs from orc: >> logs/after-test-docker-logs.txt
docker logs orc >> logs/after-test-docker-logs.txt
echo '' >> logs/after-test-docker-logs.txt
docker logs orc


echo After-test logs from wordle-api-tester >> logs/after-test-docker-logs.txt
docker logs wordle-api-tester >> logs/after-test-docker-logs.txt
docker logs wordle-api-tester

# cat logs/after-test-docker-logs.txt
echo view logs in logs/after-test-docker-logs.txt