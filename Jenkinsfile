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
        echo 'building the application..'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          cat .env
          cp .env app/services/Stats/.env
          ls -al app/services/Stats/
          ls -al
        '''
        sh'''
          docker ps
          docker ps -a
          docker rm stats-cont
          docker ps -a
        '''
        // sh '''
        //   docker build -t w-stats ./app/services/Stats
        //   docker run --name stats-cont w-stats
        // '''
        // sh'''
        //   docker build -t w-stats ./app/services/Stats
        //   docker run --name stats-cont w-stats
        //   curl localhost:9000
        //   docker build -t w-wordcheck ./app/services/WordCheck
        //   docker build -t w-wordvalidation ./app/services/WordValidation
        //   docker build -t w-play ./app/services/Play
        //   docker build -t w-orc .
        //   docker run --name wordcheck-cont w-wordcheck
        //   docker run --name wordvalidation-cont w-wordvalidation
        //   docker run --name play-cont w-play
        //   docker run --name orc-cont w-orc
        // '''
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
        // sh '''
        //   curl google.com
        //   curl localhost:9400

        // '''
        // sh '''
        //   curl google.com
        //   sudo -s
        //   curl localhost:9000
        //   curl localhost:9100
        //   curl localhost:9200
        //   curl localhost:9300
        //   curl localhost:9400
        //   curl localhost:6379
        // '''
      }
      
    }
    
    // stage("shutdown") {

    //   steps {
    //     echo 'Shutting down containers...'
    //     // sh '''
    //     //   docker compose down
    //     // '''
    //   }
      
    // }
    
  }

}