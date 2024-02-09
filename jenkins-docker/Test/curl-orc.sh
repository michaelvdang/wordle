## called when the wordle-api-tester container is run
echo UTC date and time: `date +%m-%d\ %T` > /data/output.txt
## scenario 1: 
# 1. Generate random username and Create new game with username (Create new game)
# 2. Add 1 guess (Add guess)
# 3. Ask for a new game (Create new game)
# 4. Add 1 guess in new game (Add guess)
# 5. Return to game which does not exist (Restore game 1)
# 6. Restore to previous game (Restore game)
# 6. Finish this game by adding 5 more guesses (Add guess)

USERNAME=`bash random-string.sh`
# USERNAME='ucohen'
echo username is: $USERNAME
echo start first new game URL: "orc:9400/game/new?username=${USERNAME}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" > /data/curl_results.txt
GUID=`cat /data/curl_results.txt | jq '.guid' | tr -d '"'`
echo guid is: $GUID >> /data/output.txt
GAME_ID1=`cat /data/curl_results.txt | jq '.game_id'`
echo game_id1 is $GAME_ID1 >> /data/output.txt
USER_ID=`cat /data/curl_results.txt | jq '.user_id'`
echo user_id is $USER_ID >> /data/output.txt

GUESS=house
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
echo Start second new game URL: "orc:9400/game/new?username=${USERNAME}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" > /data/curl_results.txt
GAME_ID2=`cat /data/curl_results.txt | jq '.game_id'`
echo game_id2 is $GAME_ID2 >> /data/output.txt

GUESS=homie
echo The guess word is $GUESS >> /data/output.txt
echo The Add Guess URL will be: "orc:9400/game/${GAME_ID2}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID2}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
echo Restoring to a game which does not exist game_id == 1 >> /data/output.txt
echo The Restore Game URL will be: "'orc:9400/game/restore?username=${USERNAME}&game_id=1'" >> /data/output.txt
curl --no-progress-meter -X 'POST' "'orc:9400/game/restore?username=${USERNAME}&game_id=1'" >> /data/output.txt
echo ''
echo Restoring to the original game: >> /data/output.txt
echo The Restore Game URL will be: "'orc:9400/game/restore?username=${USERNAME}&game_id=$GAME_ID1'" >> /data/output.txt
curl --no-progress-meter -X 'POST' "'orc:9400/game/restore?username=${USERNAME}&game_id=$GAME_ID1'" >> /data/output.txt
echo ''
echo Finish the original game: >> /data/output.txt
GUESS=angrier
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=angries
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=angry
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=paint
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=rhyme
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=learn
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=share
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''
GUESS=plant
echo The guess word is $GUESS >> /data/output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/output.txt
echo ''


# curl --no-progress-meter 'wordvalidation:9200/' >> /data/output.txt
# curl --no-progress-meter 'wordvalidation:9200/word/is-valid/house' >> /data/output.txt
# curl --no-progress-meter 'orc:9400/game/restore?username=ucohen&game_id=100' >> /data/output.txt
# curl --no-progress-meter 'play:9300/play?guid=al%3Bskdjf&game_id=100' >> /data/output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/count' >> /data/output.txt
# curl --no-progress-meter 'wordcheck:9100/answers/correct?game_id=100' >> /data/output.txt

# curl -X 'POST' 'orc:9400/game/new?username=ucohen'
# curl -X 'POST' 'orc:9400/game/new?username=ucohen' -H 'accept: application/json' -d '' > first_curl.txt
