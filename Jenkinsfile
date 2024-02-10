pipeline {
  agent any
  environment {
    ENV_FILE_PATH = credentials('wordle-env-file')
    REDIS_CONF_FILE_PATH = credentials('redis-conf-file')
    REDIS_SECRET = credentials('redis-secret')
  }
  stages {
    stage("precheck") {
      steps {
        sh 'chmod u+x -R ./jenkins-docker'
        sh './jenkins-docker/Pre-Build/pre-build.sh'
        echo 'Confirm .env and redis.conf file content: '
        archiveArtifacts '.env'
        archiveArtifacts 'app/services/Redis/redis.conf'
        sh 'printenv'
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
      sh './jenkins-docker/Post/post.sh'
    }
    // failure {
    //   sh 'jenkins-docker/post.sh'
    // }
  }
}