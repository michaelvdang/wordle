docker run -d --name ubuntu-tester --network wordle-network ubuntu-image
curl -X 'POST' \
  'orc:9400/game/new?username=ucohen' \
  -H 'accept: application/json' \
  -d '' > first_curl.txt

