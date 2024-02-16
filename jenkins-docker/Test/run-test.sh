## to be run on a Linux Jenkins agent with docker installed
echo ===================Testing the api===================
# TopTen.py must run through a python container
echo Prepare Redis leaderboard:
docker exec orc python3 /wordle/bin/TopTen.py

echo 'Ping Redis...'
docker exec redis redis-cli -a "$REDIS_SECRET" ping
echo ''

# API integration testing
echo 'Buidling wordle-api-tester...'
ls -al logs
mkdir -p logs
chmod +w logs
ls -al logs
docker build   --progress=plain -t wordle-api-tester-image ./jenkins-docker/Test/integration-api-test/
docker run -d --volume ./logs/:/data --name wordle-api-tester --network wordle-network wordle-api-tester-image


