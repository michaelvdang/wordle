## to be run inside a Docker image of ubuntu:jammy with curl installed
curl stats:9000 > conn-status.txt 
echo '' >> conn-status.txt
curl wordcheck:9100 >> conn-status.txt 
echo '' >> conn-status.txt
curl wordvalidation:9200 >> conn-status.txt 
echo '' >> conn-status.txt
curl play:9300 >> conn-status.txt 
echo '' >> conn-status.txt
curl orc:9400 >> conn-status.txt
