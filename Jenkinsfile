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
        // sh '''
        //   pwd
        //   ls -al app/services/Stats
        //   echo ${ENV_FILE_CONTENT} > ./.env
        //   echo ${REDIS_CONF_CONTENT} > ./redis.conf
        //   cat .env | base64 
        //   ls -al app/services/Stats/
        //   cp .env app/services/Stats/.env
        //   ls -al app/services/Stats/
        //   ls -al
        // '''
        // sh '''
        //   docker rm -f stats  # containers don't get removed when there's a crash
        //   docker rmi -f stats-image
        //   docker build -t stats-image ./app/services/Stats
        //   docker run -d --rm --name stats -p 9000:9000 -h localhost --network test-network stats-image
        //   docker inspect stats
        // '''
        // echo 'Building WordCheck container...'
        // sh '''
        //   docker rm -f wordcheck
        //   docker rmi -f wordcheck-image
        //   docker build -t wordcheck-image ./app/services/WordCheck
        //   docker run -d --rm --name wordcheck -p 9100:9100 -h localhost --network test-network  wordcheck-image
        // '''
        // echo 'Building WordValidation container...'
        // sh '''
        //   docker rm -f wordvalidation
        //   docker rmi -f wordvalidation-image
        //   docker build -t wordvalidation-image ./app/services/WordValidation
        //   docker run -d --rm --name wordvalidation -p 9200:9200 -h localhost --network test-network wordvalidation-image
        // '''
        // echo 'Building play container...'
        // sh '''
        //   docker rm -f play
        //   docker rmi -f play-image
        //   docker build -t play-image ./app/services/Play
        //   docker run -d --rm --name play -p 9300:9300 -h localhost --network test-network play-image
        // '''
        // echo 'Building orc container...'
        // sh '''
        //   docker rm -f orc
        //   docker rmi -f orc-image
        //   docker build -t orc-image .
        //   docker run -d --rm --name orc -p 9400:9400 -h localhost --network test-network orc-image
        // '''
        // sh 'docker build -t ubuntu-image ./jenkins-docker/'
        // sh '''
        //   docker run -d --rm --name ubuntu-tester --network test-network ubuntu-image
        // '''
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
          docker images
          docker rmi 8f505f4bae41 b32f0c9b815c
        '''
      }
    }
    
    stage("shutdown") {

      steps {
        echo 'Shutting down containers...'
        sh '''
          docker ps
          docker ps -a
          docker stop stats
          docker stop wordcheck
          docker stop wordvalidation
          docker stop play
          docker stop orc
          docker ps 
          docker ps -a
          docker images
          docker images -f dangling=true
          docker image prune -f
          docker images
          docker rmi stats-image
          docker rmi wordcheck-image
          docker rmi wordvalidation-image
          docker rmi play-image
          docker rmi orc-image
          docker rmi ubuntu-image
        '''
      }
      
    }
    
  }

}