# deploy must SSH onto server, currently the only way is to use scripted pipeline
# so we must use another Jenkins job that uses scripted (instead of declarative) pipeline
# setup Jenkins with the SSH credential for the VPS with id: AWS-EC2
# change the <IP_ADDRESS> in the Wordle-deploy Jenkinsfile to the correct address

sh '''
ls -al
IP_ADDRESS=1.2.3.4
echo $IP_ADDRESS
'''