## called when the wordle-api-tester container is run
echo `date +%m-%d\ %T` > /data/output.txt
USERNAME='ucohen'
echo first URL: "orc:9400/game/new?username=${USERNAME}"
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" >> /data/output.txt
GUID=`cat /data/output.txt | jq '.guid' | tr -d '"'`
echo guid is: $GUID
GAME_ID=`cat /data/output.txt | jq '.game_id'`
echo game_id is $GAME_ID
USER_ID=`cat /data/output.txt | jq '.user_id'`
echo user_id is $USER_ID

sleep 3
GUESS=house
echo guess is $GUESS
echo the new URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}"
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

sleep 3
GUESS=angry
echo guess is $GUESS
echo the new URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}"
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

sleep 3
GUESS=paint
echo guess is $GUESS
echo the new URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}"
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

sleep 3
GUESS=rhyme
echo guess is $GUESS
echo the new URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}"
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

sleep 3
GUESS=learn
echo guess is $GUESS
echo the new URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}"
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

sleep 3
GUESS=share
echo guess is $GUESS
echo the new URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}"
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt


# curl --no-progress-meter 'wordvalidation:9200/' >> /data/output.txt
# curl --no-progress-meter 'wordvalidation:9200/word/is-valid/house' >> /data/output.txt
# curl --no-progress-meter 'orc:9400/game/restore?username=ucohen&game_id=100' >> /data/output.txt
# curl --no-progress-meter 'play:9300/play?guid=al%3Bskdjf&game_id=100' >> /data/output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/count' >> /data/output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/correct?game_id=100' >> /data/output.txt

# curl -X 'POST' 'orc:9400/game/new?username=ucohen'
# curl -X 'POST' 'orc:9400/game/new?username=ucohen' -H 'accept: application/json' -d '' > first_curl.txt
