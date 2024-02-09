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
        
        // sh 'chmod u+x -R ./jenkins-docker'
        sh 'cat $ENV_FILE_PATH > .env'
        sh 'cat $ENV_FILE_PATH > app/services/Stats/.env'
        sh 'cat $ENV_FILE_PATH > app/services/Play/.env'
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

        // // testing fastapi
        // sh '''
        //   docker ps
        //   docker ps -a
        //   docker images
        //   docker build -t fa-image ./app/services/base
        //   docker run -d --name fa-cont --network wordle-network fa-image
        //   docker build -t fa-tester-image ./jenkins-docker/test-base
        //   docker run -d --name fa-tester --network wordle-network fa-tester-image
        // '''
        // sh 'docker logs fa-tester'
        // sh 'docker logs fa-cont'
      }
    }

    stage("test") {
      steps {
        // sh 'sleep 5'
        sh './jenkins-docker/Test/test.sh'
        
      }
    }
    
  }
  post {
    always {
      // // testing fastapi
      // sh '''
      //   docker rm -f fa-cont
      //   docker rmi -f fa-image
      //   docker rm -f fa-tester
      //   docker rmi -f fa-tester-image
      // '''

      // sh 'chmod u+x jenkins-docker/post.sh'
      sh './jenkins-docker/Post/post.sh'

    }
    // failure {
    //   sh 'jenkins-docker/post.sh'
    // }
  }
}