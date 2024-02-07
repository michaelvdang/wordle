docker build -t stats-image --no-cache ../app/services/Stats
docker run -d --rm --name stats -p 9000:9000 --network test-network stats-image
docker build -t wordcheck-image ../app/services/WordCheck
docker run -d --rm --name wordcheck -p 9100:9100 -h localhost --network test-network  wordcheck-image
docker build -t wordvalidation-image ../app/services/WordValidation
docker run -d --rm --name wordvalidation -p 9200:9200 -h localhost --network test-network wordvalidation-image
docker build -t play-image ../app/services/Play
docker run -d --rm --name play -p 9300:9300 -h localhost --network test-network play-image
docker build -t orc-image ../
docker run -d --rm --name orc -p 9400:9400 -h localhost --network test-network orc-image
docker run -d --rm --name nginx-tester --network test-network nginx:alpine
pause


