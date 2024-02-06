pwd
curl stats:9000 > app.txt
curl wordcheck:9100 > app.txt
curl wordvalidation:9200 > app.txt
curl google.com > google.txt
curl play:9300 > app.txt
curl orc:9400  > app.txt

cat app.txt
cat google.txt
