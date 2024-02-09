## called when the wordle-api-tester container is run
curl --no-progress-meter -X 'POST' 'orc:9400/game/new?username=ucohen' >> output.txt
GUID=`cat output.txt | jq '.guid'`
echo $GUID
# curl --no-progress-meter 'wordvalidation:9200/' >> output.txt
# curl --no-progress-meter 'wordvalidation:9200/word/is-valid/house' >> output.txt
# curl --no-progress-meter 'orc:9400/game/restore?username=ucohen&game_id=100' >> output.txt
# curl --no-progress-meter 'play:9300/play?guid=al%3Bskdjf&game_id=100' >> output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/count' >> output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/correct?game_id=100' >> output.txt

# curl -X 'POST' 'orc:9400/game/new?username=ucohen'
# curl -X 'POST' 'orc:9400/game/new?username=ucohen' -H 'accept: application/json' -d '' > first_curl.txt
