# deploy must SSH onto server, currently the only way is to use scripted pipeline
# so we must use another Jenkins job that uses scripted (instead of declarative) pipeline
# setup Jenkins with the SSH credential for the VPS with id: AWS-EC2
# change the <IP_ADDRESS> in the Wordle-deploy Jenkinsfile to the correct address

# don't forget to mount the Jenkinsfile to orc container when it is run
# docker exec orc python3 /wordle/jenkins-docker/Deploy/update-pre-deploy-Jenkinsfile.py
# cat ./jenkins-docker/Deploy/Jenkinsfile

docker exec orc ls -al /wordle/jenkins-docker/Deploy
docker exec orc python3 /wordle/jenkins-docker/Deploy/extract-ip-address.py
IP_ADDRESS=`cat ./jenkins-docker/Deploy/IP_ADDRESS.env`
echo $IP_ADDRESS
docker exec orc rm /wordle/jenkins-docker/Deploy/IP_ADDRESS.env