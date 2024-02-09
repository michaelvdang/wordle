curl --no-progress-meter 'wordvalidation:9200/' > wv.txt
curl --no-progress-meter 'wordvalidation:9200/fake-endpoint' >> wv.txt
curl -s 'wordvalidation:9200/word/is-valid/house' >> wv.txt
curl 'orc:9400/game/restore?username=ucohen&game_id=100' >> /output/orc.txt
curl 'play:9300/play?guid=al%3Bskdjf&game_id=100' >> /output/play.txt
curl 'wordcheck:9100/answers/count' >> /output/wc.txt
curl 'wordcheck:9100/answers/correct?game_id=100' >> /output/wc.txt

# curl -X 'POST' 'orc:9400/game/new?username=ucohen'
# curl -X 'POST' 'orc:9400/game/new?username=ucohen' -H 'accept: application/json' -d '' > first_curl.txt
