pipeline {
  agent any
  environment {
    ENV_FILE_CONTENT = credentials('wordle-env-file')
    REDIS_CONF_CONTENT = credentials('redis-conf')
  }
  stages {
    stage("precheck") {
      steps {
        sh 'chmod u+x -R ./jenkins-docker'
        sh 'echo $ENV_FILE_CONTENT'
        sh 'ls -al'
        sh 'echo ${ENV_FILE_CONTENT} > ./.env'
        sh 'echo ${REDIS_CONF_CONTENT} > ./redis.conf'
        sh 'ls -al'
        sh 'cat .env | base64'
        // sh '''
        //   echo Putting .env content from Credentials into files for containers to use...
        //   pwd
        //   ls -al
        //   echo ${ENV_FILE_CONTENT} > ./.env
        //   echo ${REDIS_CONF_CONTENT} > ./redis.conf
        //   ls -al
        //   echo DONE.
        //   cat .env | base64
        //   cat redis.conf | base64
        // '''
        
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
        sh './jenkins-docker/Test/test.sh'
      }
    }
    
  }
  post {
    always {
      // sh 'chmod u+x jenkins-docker/post.sh'
      sh './jenkins-docker/post.sh'
    }
    // failure {
    //   sh 'jenkins-docker/post.sh'
    // }
  }
}