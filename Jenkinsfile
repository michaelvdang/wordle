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
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          cat .env
          cp .env app/services/Stats/.env
          ls -al app/services/Stats/
          ls -al
        '''
        sh '''
          docker rm -f stats-cont
          docker build -t w-stats ./app/services/Stats
          docker run -d --name stats-cont w-stats
        '''
      }
      steps {
        echo 'Building WordCheck container...'
        sh '''
          docker rm -f wordcheck-cont
          docker build -t w-wordcheck ./app/services/WordCheck
          docker run -d --name wordcheck-cont w-wordcheck
        '''
      }
      steps {
        echo 'Building WordValidation container...'
        sh '''
          docker rm -f wordvalidation-cont
          docker build -t w-wordvalidation ./app/services/WordValidation
          docker run -d --name wordvalidation-cont w-wordvalidation
        '''
      }
      steps {
        echo 'Building play container...'
        sh '''
          docker rm -f play-cont
          docker build -t w-play ./app/services/Play
          docker run -d --name play-cont w-play
        '''
      }
      steps {
        echo 'Building orc container...'
        sh '''
          docker rm -f orc-cont
          docker build -t w-orc .
          docker run -d --name orc-cont w-orc
        '''
      }
    }

    stage("test") {
      steps {
        echo 'testing the env files..'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          docker ps -a
        '''
        sh '''
          curl google.com
          curl localhost:9400
        '''
      }
    }
    
    stage("shutdown") {

      steps {
        echo 'Shutting down containers...'
        sh '''
          docker ps
          docker ps -a
          docker stop stats-cont
          docker rm stats-cont
          docker stop wordcheck-cont
          docker rm wordcheck-cont
          docker stop wordvalidation-cont
          docker rm wordvalidation-cont
          docker stop play-cont
          docker rm play-cont
          docker stop orc-cont
          docker rm orc-cont
          docker ps 
          docker ps -a
        '''
      }
      
    }
    
  }

}