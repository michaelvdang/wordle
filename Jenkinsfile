pipeline {
  agent any
  environment {
    ENV_FILE_CONTENT = credentials('wordle-env-file')
    REDIS_CONF_CONTENT = credentials('redis-conf')
  }
  stages {
    stage("precheck") {
      steps {
        sh '''
          echo Putting .env content from Credentials into files for containers to use...
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          echo DONE.
        '''
        // sh 'printenv'
      }
    }
    stage("build") {
      steps {
        sh './jenkins-docker/build.sh'
      }
    }

    stage("test") {
      steps {
        echo 'testing the env files..'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
        '''
      }
    }
    
  }
  post {
    always {
      sh 'chmod u+x jenkins-docker/post.sh'
      sh './jenkins-docker/post.sh'
    }
    // failure {
    //   sh 'jenkins-docker/post.sh'
    // }
  }
}