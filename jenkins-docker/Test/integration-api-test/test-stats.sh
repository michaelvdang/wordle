## to be run inside a Docker container with curl and jq
echo ''
echo UTC date and time: `date +%m-%d\ %T` > /data/stats-output.txt
echo Testing stats API >> /data/stats-output.txt
## Testing all endpoints in the stats API, success scenario

echo Querying top streaks and winners: stats:9000/stats/top-streaks-and-winners >> /data/stats-output.txt
curl stats:9000/stats/top-streaks-and-winners >> /data/stats-output.txt
echo '' >> /data/stats-output.txt
echo Querying top streaks: stats:9000/stats/top-streaks >> /data/stats-output.txt
curl stats:9000/stats/top-streaks >> /data/stats-output.txt
echo '' >> /data/stats-output.txt
echo Querying top winners: stats:9000/stats/top-winners >> /data/stats-output.txt
curl stats:9000/stats/top-winners >> /data/stats-output.txt

## scenario 1: Success
# 1. Create random user (/stats/users/new)
# 2. Get user id
# 3. Get user stats
# 4. Get username
# 5. Create new game
# 6. Add 6 guesses to complete game
# 7. Get user stats (testing /stats/games/store-result)

USERNAME=`bash random-string.sh`
echo '' >> /data/stats-output.txt
echo New username to create: $USERNAME >> /data/stats-output.txt
echo 'Create User (/stats/users/new)' >> /data/stats-output.txt
curl -X POST "stats:9000/stats/users/new?username=${USERNAME}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

echo Get user id - URL: "stats:9000/stats/id/${USERNAME}" >> /data/stats-output.txt
curl "stats:9000/stats/id/${USERNAME}" > /data/stats-curl-results.txt
USER_ID=`cat /data/stats-curl-results.txt | jq '.user_id' | tr -d '"' `
cat /data/stats-curl-results.txt >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

echo Get user stats - URL: "stats:9000/stats/username/${USER_ID}" >> /data/stats-output.txt
curl "stats:9000/stats/username/${USER_ID}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

echo Create new game - URL: "orc:9400/game/new?username=${USERNAME}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/new?username=${USERNAME}" > /data/orc-curl-results.txt
GUID=`cat /data/orc-curl-results.txt | jq '.guid' | tr -d '"'`
echo guid is: $GUID >> /data/stats-output.txt
GAME_ID1=`cat /data/orc-curl-results.txt | jq '.game_id'`
echo game_id1 is $GAME_ID1 >> /data/stats-output.txt
USER_ID=`cat /data/orc-curl-results.txt | jq '.user_id'`
echo user_id is $USER_ID >> /data/stats-output.txt 
echo '' >> /data/stats-output.txt

GUESS=angry
echo The guess word is $GUESS >> /data/stats-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

GUESS=paint
echo The guess word is $GUESS >> /data/stats-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

GUESS=rhyme
echo The guess word is $GUESS >> /data/stats-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

GUESS=learn
echo The guess word is $GUESS >> /data/stats-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

GUESS=share
echo The guess word is $GUESS >> /data/stats-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

GUESS=plant
echo The guess word is $GUESS >> /data/stats-output.txt
echo the Add Guess URL will be: "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
curl --no-progress-meter -X 'POST' "orc:9400/game/${GAME_ID1}?username=${USERNAME}&guid=${GUID}&user_id=${USER_ID}&guess=${GUESS}" >> /data/stats-output.txt
echo '' >> /data/stats-output.txt

echo Get user stats - URL: "stats:9000/stats/user?user_id=${USER_ID}&username=${USERNAME}" >> /data/stats-output.txt
curl "stats:9000/stats/users?user_id=${USER_ID}&username=${USERNAME}" >> /data/stats-output.txt

cat /data/stats-output.txt
