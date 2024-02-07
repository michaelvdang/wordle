pipeline {
  agent any
  environment {
    ENV_FILE_CONTENT = credentials('wordle-env-file')
    REDIS_CONF_CONTENT = credentials('redis-conf')
  }
  stages {
    stage("build") {
      steps {
        // sh 'printenv'
        echo 'building Stats container..'
        sh '''
          pwd
          ls -al
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          ls -al
          cat .env | base64 
          ls -al app/services/Stats/
          cp .env app/services/Stats/.env
          ls -al app/services/Stats/
          docker ps
          docker network inspect test-network
        '''
        sh '''
          docker rm -f stats  # containers don't get removed when there's a crash
          docker rmi -f stats-image
          docker build --no-cache -t stats-image ./app/services/Stats
          docker run -d --rm --name stats -p 9000:9000 --network test-network stats-image
          docker inspect stats | grep Status
          sleep 5
          docker inspect stats | grep Status
        '''
        echo 'Building WordCheck container...'
        sh '''
          docker rm -f wordcheck
          docker rmi -f wordcheck-image
          docker build --no-cache -t wordcheck-image ./app/services/WordCheck
          docker run -d --rm --name wordcheck -p 9100:9100 -h localhost --network test-network  wordcheck-image
        '''
        echo 'Building WordValidation container...'
        sh '''
          docker rm -f wordvalidation
          docker rmi -f wordvalidation-image
          docker build --no-cache -t wordvalidation-image ./app/services/WordValidation
          docker run -d --rm --name wordvalidation -p 9200:9200 -h localhost --network test-network wordvalidation-image
        '''
        echo 'Building play container...'
        sh '''
          docker rm -f play
          docker rmi -f play-image
          docker build --no-cache -t play-image ./app/services/Play
          docker run -d --rm --name play -p 9300:9300 -h localhost --network test-network play-image
        '''
        echo 'Building orc container...'
        sh '''
          docker rm -f orc
          docker rmi -f orc-image
          docker images
          docker ps
          docker build --no-cache -t orc-image .
          docker run -d --rm --name orc -p 9400:9400 -h localhost --network test-network orc-image
        '''
        sh '''
          docker rmi -f ubuntu-image 095e68df905a
          docker build --no-cache -t nginx-tester-image ./jenkins-docker/
          docker run -d --rm --name nginx-tester --network test-network nginx-tester-image
        '''
      }
    }

    stage("test") {
      steps {
        echo 'testing the env files..'
        sh'sleep 5'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          docker ps -a
        '''
      }
    }
    
    stage("shutdown") {

      steps {
        echo 'Shutting down containers...'
        sh '''
          docker images
          docker ps
          docker ps -a
        '''
        // sh 'docker stop stats'
        // sh 'docker rmi -f stats-image'
        // sh 'docker stop wordcheck'
        // sh 'docker rmi -f wordcheck-image'
        // sh 'docker stop wordvalidation'
        // sh 'docker rmi -f wordvalidation-image'
        // sh 'docker stop play'
        // sh 'docker rmi -f play-image'
        // sh 'docker stop orc'
        // sh 'docker rmi -f orc-image'
        // sh 'docker stop ubuntu-tester'
        // sh 'docker rmi -f ubuntu-image'
        sh '''
          docker ps 
          docker ps -a
          docker images
          docker images -f dangling=true
          docker image prune -f
          docker images
        '''

      }
      
    }
    
  }

}