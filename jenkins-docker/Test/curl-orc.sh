curl 'wordvalidation:9200/word/is-valid/house' > wv.txt
curl 'orc:9400/game/restore?username=ucohen&game_id=2' > orc.txt
curl -X 'POST' 'orc:9400/game/new?username=ucohen'
# curl -X 'POST' 'orc:9400/game/new?username=ucohen' -H 'accept: application/json' -d '' > first_curl.txt
