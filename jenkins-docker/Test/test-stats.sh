echo ''
echo UTC date and time: `date +%m-%d\ %T` > /data/stats-output.txt
## Testing 3 endpoints in the stats API: Get User Stats, Get Username, Get User Id
## scenario 1:
# 1. Create random user
# 2. 
# 2. Create new game
# 3. Add 6 guesses to complete game

echo Querying top streaks and winners: stats:9000/stats/top-streaks-and-winners >> /data/stats-output.txt
curl stats:9000/stats/top-streaks-and-winners >> /data/stats-output.txt

USERNAME=`bash random-string.sh`



cat /data/stats-output.txt