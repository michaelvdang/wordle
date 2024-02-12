import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.environ.get('SERVER_IP')

with open(r'/wordle/jenkins-docker/Deploy/Jenkinsfile', 'w') as file:
  file.write(SERVER_IP)

print('SERVER_IP extracted')