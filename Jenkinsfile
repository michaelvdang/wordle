pipeline {

  // agent { label "linux" }
  agent any

  stages {

    stage("build") {

      environment {
        ENV_FILE_CONTENT = credentials('wordle-env-file')
        REDIS_CONF_CONTENT = credentials('redis-conf')
      }

      steps {
        sh 'printenv'
        echo 'building the application..'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          ls -al
          
          # installing Docker according to https://docs.docker.com/engine/install/ubuntu/
          for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
          
          # Add Docker's official GPG key:
          sudo apt-get update
          sudo apt-get install ca-certificates curl
          sudo install -m 0755 -d /etc/apt/keyrings
          sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
          sudo chmod a+r /etc/apt/keyrings/docker.asc

          # Add the repository to Apt sources:
          echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
            $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
            sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
          sudo apt-get update

          sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
          # finished installing Docker
          
          docker compose up -d 
        '''
      }
      
    }

    stage("test") {

      steps {
        echo 'testing the application..'
        sh '''
          curl localhost:9000
          curl localhost:9100
          curl localhost:9200
          curl localhost:9300
          curl localhost:9400
          curl localhost:6379
        '''
      }
      
    }
    
    stage("shutdown") {

      steps {
        sh '''
          docker compose down
        '''
      }
      
    }
    
  }

}