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
      }
    }
    stage("build") {
      steps {
        sh './jenkins-docker/build.sh'
      }
    }
    stage("test") {
      steps {
        sh './jenkins-docker/Test/run-test.sh'
      }
    }
    stage("pre-deploy") {
      steps {
        sh './jenkins-docker/Deploy/pre-deploy.sh'
      }
    }
  }
  post {
    always {
      sh './jenkins-docker/Post/post.sh'
    }
  }
}