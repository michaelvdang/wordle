## called when the wordle-api-tester container is run
echo UTC date and time: `date +%m-%d\ %T` > /data/orc-output.txt
echo Testing orc API >> /data/orc-output.txt
curl "orc:9400" >> /data/orc-output.txt
curl "check:9100" >> /data/orc-output.txt
curl "check:9100/answers/count" >> /data/orc-output.txt
curl "validation:9200" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt
## scenario 1: 
# 1. Generate random username and Create new game with username (Create new game)
# 2. Add 1 guess (Add guess)
# 3. Ask for a new game (Create new game)
# 4. Add 1 guess in new game (Add guess)
# 5. Return to game which does not exist (Restore game 1)
# 6. Restore to previous game (Restore game)
# 6. Finish this game by adding 5 more guesses (Add guess)

USERNAME=`./random-string.sh`
# USERNAME='ucohen'
echo username is: $USERNAME >> /data/orc-output.txt
echo start first new game URL: "orc:9400/game/new?username=${USERNAME}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" > /data/curl_results.txt
GUID=`cat /data/curl_results.txt | jq '.guid' | tr -d '"'`
echo guid is: $GUID >> /data/orc-output.txt
GAME_ID1=`cat /data/curl_results.txt | jq '.game_id'`
echo game_id1 is $GAME_ID1 >> /data/orc-output.txt
USER_ID=`cat /data/curl_results.txt | jq '.user_id'`
echo user_id is $USER_ID >> /data/orc-output.txt

GUESS=house
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt
echo Start second new game URL: "orc:9400/game/new?username=${USERNAME}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" > /data/curl_results.txt
GAME_ID2=`cat /data/curl_results.txt | jq '.game_id'`
echo game_id2 is $GAME_ID2 >> /data/orc-output.txt

GUESS=homie
echo The guess word is $GUESS >> /data/orc-output.txt
echo The Add Guess URL will be: "orc:9400/game/${GAME_ID2}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID2}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
# Restore
echo '' >> /data/orc-output.txt

echo Restoring to a game which does not exist game_id == 1 >> /data/orc-output.txt
echo The Restore Game URL will be: "orc:9400/game/restore?username=${USERNAME}&game_id=1" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/restore?username=${USERNAME}&game_id=1" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

echo Restoring to the original game: >> /data/orc-output.txt
echo The Restore Game URL will be: "orc:9400/game/restore?username=${USERNAME}&game_id=$GAME_ID1" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/restore?username=${USERNAME}&game_id=$GAME_ID1" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

echo Finish the original game: >> /data/orc-output.txt
GUESS=angrier
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=angries
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=angry
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=paint
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=rhyme
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=learn
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=share
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt

GUESS=plant
echo The guess word is $GUESS >> /data/orc-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/orc-output.txt
echo '' >> /data/orc-output.txt


cat /data/orc-output.txt
