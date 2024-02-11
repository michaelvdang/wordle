import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.environ.get('SERVER_IP')

placeholder = '<IP_ADDRESS>'

with open(r'/wordle/jenkins-docker/Deploy/Jenkinsfile', 'r') as file:
  data = file.read()

  data = data.replace(placeholder, SERVER_IP)

with open(r'/wordle/jenkins-docker/Deploy/Jenkinsfile', 'w') as file:
  file.write(data)

print('Text replaced')