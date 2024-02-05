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
          ls -al app/services/Stats
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          cat .env
          cp .env app/services/Stats/.env
          ls -al app/services/Stats/
          ls -al
        '''
        sh '''
          docker rm -f stats-cont
          docker rmi -f w-stats
          docker build -t w-stats ./app/services/Stats
          docker run -d --name stats-cont -p 9000:9000 -h localhost --network test-network w-stats
          docker inspect stats-cont
        '''
        // echo 'Building WordCheck container...'
        // sh '''
        //   docker rm -f wordcheck-cont
        //   docker build -t w-wordcheck ./app/services/WordCheck
        //   docker run -d --name wordcheck-cont -p 9100:9100 -h localhost  w-wordcheck
        // '''
        // echo 'Building WordValidation container...'
        // sh '''
        //   docker rm -f wordvalidation-cont
        //   docker build -t w-wordvalidation ./app/services/WordValidation
        //   docker run -d --name wordvalidation-cont -p 9200:9200 -h localhost w-wordvalidation
        // '''
        // echo 'Building play container...'
        // sh '''
        //   docker rm -f play-cont
        //   docker build -t w-play ./app/services/Play
        //   docker run -d --name play-cont -p 9300:9300 -h localhost w-play
        // '''
        // echo 'Building orc container...'
        // sh '''
        //   docker rm -f orc-cont
        //   docker build -t w-orc .
        //   docker run -d --name orc-cont -p 9400:9400 -h localhost w-orc
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
        '''
        // sh'curl 127.0.0.1:9000'
        // sh'curl -s localhost:9000'
        sh'curl -s stats-cont:9000'
        sh'curl -s dde366b98c3e:9000'
        sh'curl -s 127.0.0.1:9000'
        // sh '''
        //   curl google.com
        //   curl localhost:9000
        //   curl localhost:9100
        //   curl localhost:9200
        //   curl localhost:9300
        //   curl localhost:9400
        // '''
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