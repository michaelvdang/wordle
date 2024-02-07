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
        sh 'docker network create wordle-network'
        echo 'building Stats container..'
        sh '''
          docker build    -t stats-image ./app/services/Stats
          docker run -d --name stats -p 9000:9000 --network wordle-network stats-image
        '''
        echo 'Building WordCheck container...'
        sh '''
          docker build    -t wordcheck-image ./app/services/WordCheck
          docker run -d --name wordcheck -p 9100:9100 -h localhost --network wordle-network  wordcheck-image
        '''
        echo 'Building WordValidation container...'
        sh '''
          docker build    -t wordvalidation-image ./app/services/WordValidation
          docker run -d --name wordvalidation -p 9200:9200 -h localhost --network wordle-network wordvalidation-image
        '''
        echo 'Building play container...'
        sh '''
          docker build    -t play-image ./app/services/Play
          docker run -d --name play -p 9300:9300 -h localhost --network wordle-network play-image
        '''
        echo 'Building orc container...'
        sh '''
          docker build    -t orc-image .
          docker run -d --name orc -p 9400:9400    --network wordle-network orc-image
        '''
        sh '''
          docker build    -t ubuntu-image ./jenkins-docker/
          docker run -d --name ubuntu-tester --network wordle-network ubuntu-image
        '''
        sh 'docker logs orc'
        echo 'Containers in wordle-network:'
        sh 'docker network inspect --format=\'{{range $container_id,$conf := .Containers}} {{println $conf.Name $container_id}} {{end}}\' wordle-network'
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