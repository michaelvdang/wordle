# curl orc:9400 >> output.txt
curl stats:9000 > output.txt 
echo -e '\n'
curl wordcheck:9100 >> output.txt 
echo -e '\n'
curl wordvalidation:9200 >> output.txt 
echo -e '\n'
curl play:9300 >> output.txt 
echo -e '\n'
curl orc:9400 >> output.txt
