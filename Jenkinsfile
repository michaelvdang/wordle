pipeline {

  // agent { label "linux" }
  agent any
  // agent { 
  //   dockerfile true 
  //   // reuseNode true
  // }

  stages {

    stage("build") {
      agent { 
        dockerfile {
          filename 'Dockerfile'
          dir './'
          // args '--volumes-from db079cc9888d74d020f35c70a0ff1be8859dfa6416d1d4c14d09abfdff6e9602 -v /var/jenkins_home/workspace/wordle_docker-jenkins:/var/jenkins_home/workspace/wordle_docker-jenkins:rw,z -v /var/jenkins_home/workspace/wordle_docker-jenkins@tmp:/var/jenkins_home/workspace/wordle_docker-jenkins@tmp:rw,z -w /var/jenkins_home/workspace/wordle_docker-jenkins'
          reuseNode true
        }
      }

      environment {
        ENV_FILE_CONTENT = credentials('wordle-env-file')
        REDIS_CONF_CONTENT = credentials('redis-conf')
      }

      steps {
        // sh 'printenv'
        echo 'building the application..'
        sh '''
          pwd
          echo ${ENV_FILE_CONTENT} > ./.env
          echo ${REDIS_CONF_CONTENT} > ./redis.conf
          cat .env
          ls -al
          whoami
          echo 'finished'
        '''
      }
      
    }

    // stage("test") {

    //   steps {
    //     echo 'testing the application..'
    //     // sh '''
    //     //   curl google.com
    //     //   sudo -s
    //     //   curl localhost:9000
    //     //   curl localhost:9100
    //     //   curl localhost:9200
    //     //   curl localhost:9300
    //     //   curl localhost:9400
    //     //   curl localhost:6379
    //     // '''
    //   }
      
    // }
    
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