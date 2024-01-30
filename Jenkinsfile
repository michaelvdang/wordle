pipeline {

  // agent { label "linux" }
  // agent any
  agent { dockerfile true }

  stages {

    stage("build") {

      environment {
        ENV_FILE_CONTENT = credentials('wordle-env-file')
        REDIS_CONF_CONTENT = credentials('redis-conf')
      }

      steps {
        // sh 'printenv'
        echo 'building the application..'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          cat .env
          ls -al
          whoami
          docker compose up -d
        '''
      }
      
    }

    stage("test") {

      steps {
        echo 'testing the application..'
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
    
    stage("shutdown") {

      steps {
        echo 'Shutting down containers...'
        // sh '''
        //   docker compose down
        // '''
      }
      
    }
    
  }

}