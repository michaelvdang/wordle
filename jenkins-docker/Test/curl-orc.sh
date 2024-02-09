## called when the wordle-api-tester container is run
echo `date +%m-%d\ %T` > /data/output.txt
USERNAME='ucohen'
echo start new game URL: "orc:9400/game/new?username=${USERNAME}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" > /data/curl_results.txt
GUID=`cat /data/curl_results.txt | jq '.guid' | tr -d '"'`
echo guid is: $GUID >> /data/output.txt
GAME_ID=`cat /data/curl_results.txt | jq '.game_id'`
echo game_id is $GAME_ID >> /data/output.txt
USER_ID=`cat /data/curl_results.txt | jq '.user_id'`
echo user_id is $USER_ID >> /data/output.txt

GUESS=house
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=angrier
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=angries
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=angry
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=paint
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=rhyme
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=learn
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt

GUESS=share
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt



# curl --no-progress-meter 'wordvalidation:9200/' >> /data/output.txt
# curl --no-progress-meter 'wordvalidation:9200/word/is-valid/house' >> /data/output.txt
# curl --no-progress-meter 'orc:9400/game/restore?username=ucohen&game_id=100' >> /data/output.txt
# curl --no-progress-meter 'play:9300/play?guid=al%3Bskdjf&game_id=100' >> /data/output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/count' >> /data/output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/correct?game_id=100' >> /data/output.txt

# curl -X 'POST' 'orc:9400/game/new?username=ucohen'
# curl -X 'POST' 'orc:9400/game/new?username=ucohen' -H 'accept: application/json' -d '' > first_curl.txt
