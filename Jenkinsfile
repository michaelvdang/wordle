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
          ls -l
          cat ./.env
          cat ./.blah
        '''
      }
      
    }

    stage("test") {

      steps {
        echo 'testing the application..'

      }
      
    }
    
  }

}