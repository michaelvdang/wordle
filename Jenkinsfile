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
          pwd
          ls -al
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          ls -al
          cat .env | base64 
          ls -al app/services/Stats/
          cp .env app/services/Stats/.env
          ls -al app/services/Stats/
        '''
      }
    }
    stage("build") {
      steps {
        // sh 'printenv'
        sh 'docker network create wordle-network'
        sh 'docker network inspect wordle-network'
        echo 'building Stats container..'
        sh '''
          docker rm -f stats  # containers don't get removed when there's a crash
          docker rmi -f stats-image
          docker build    -t stats-image ./app/services/Stats
          docker run -d --name stats -p 9000:9000 --network wordle-network stats-image
        '''
        echo 'Building WordCheck container...'
        sh '''
          docker rm -f wordcheck
          docker rmi -f wordcheck-image
          docker build    -t wordcheck-image ./app/services/WordCheck
          docker run -d --name wordcheck -p 9100:9100 -h localhost --network wordle-network  wordcheck-image
        '''
        echo 'Building WordValidation container...'
        sh '''
          docker rm -f wordvalidation
          docker rmi -f wordvalidation-image
          docker build    -t wordvalidation-image ./app/services/WordValidation
          docker run -d --name wordvalidation -p 9200:9200 -h localhost --network wordle-network wordvalidation-image
        '''
        echo 'Building play container...'
        sh '''
          docker rm -f play
          docker rmi -f play-image
          docker build    -t play-image ./app/services/Play
          docker run -d --name play -p 9300:9300 -h localhost --network wordle-network play-image
        '''
        echo 'Building orc container...'
        sh '''
          docker rm -f orc
          docker rmi -f orc-image
          docker build    -t orc-image .
          docker run -d --name orc -p 9400:9400    --network wordle-network orc-image
        '''
        sh 'sleep 5'
        sh 'docker network inspect wordle-network'
        sh 'docker logs orc'
        sh '''
          docker rm -f ubuntu-tester
          docker rmi -f ubuntu-image 095e68df905a
          docker build    -t ubuntu-image ./jenkins-docker/
          docker run -d --name ubuntu-tester --network wordle-network ubuntu-image
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
        '''
      }
    }
    
    // stage("shutdown") {
    //   steps {
    //     parallel {
    //       stats: {
    //         sh 'docker stop stats'
    //         sh 'docker rmi -f stats-image'
    //       },
    //       wordcheck: {
    //         sh 'docker stop wordcheck'
    //         sh 'docker rmi -f wordcheck-image'
    //       },
    //       wordvalidation: {
    //         sh 'docker stop wordvalidation'
    //         sh 'docker rmi -f wordvalidation-image'
    //       },
    //       play: {
    //         sh 'docker stop play'
    //         sh 'docker rmi -f play-image'
    //       },
    //       orc: {
    //         sh 'docker stop orc'
    //         sh 'docker rmi -f orc-image'
    //       },
    //       tester: {
    //         sh 'docker stop ubuntu-tester'
    //         sh 'docker rmi -f ubuntu-image'
    //       }
    //     }
    //   }
    // }
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