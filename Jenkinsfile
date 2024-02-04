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
          ls -al
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