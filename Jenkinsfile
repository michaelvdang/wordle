pipeline {
  agent any
  environment {
    ENV_FILE_PATH = credentials('wordle-env-file')
    REDIS_CONF_FILE_PATH = credentials('redis-conf-file')
  }
  stages {
    stage("precheck") {
      steps {
        sh 'chmod u+x -R ./jenkins-docker'
        sh 'cat $ENV_FILE_PATH > .env'
        sh 'cat $REDIS_CONF_FILE_PATH > app/services/Redis/redis.conf'
        echo 'Confirm .env and redis.conf file content: '
        archiveArtifacts '.env'
        archiveArtifacts 'app/services/Redis/redis.conf'
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