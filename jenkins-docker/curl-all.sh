# curl orc:9400 >> output.txt
curl stats:9000 > output.txt 
echo '' >> output.txt
curl wordcheck:9100 >> output.txt 
echo '' >> output.txt
curl wordvalidation:9200 >> output.txt 
echo '' >> output.txt
curl play:9300 >> output.txt 
echo '' >> output.txt
curl orc:9400 >> output.txt
