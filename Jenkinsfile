def remote = [:]
remote.name = "EC2 instance"

remote.allowAnyHosts = true
// create credential in Jenkins for EC2 container with id of AWS-EC2 using private key for the container
node {
  currentBuild.result = "SUCCESS"
  try {
    stage("Checkout") {
      // cleanWs()
      checkout scm
    }
    withCredentials([file(credentialsId: 'wordle-env-file', variable: 'ENV_FILE_PATH'), file(credentialsId: 'redis-conf-file', variable: 'REDIS_CONF_FILE_PATH'), string(credentialsId: 'redis-secret', variable: 'REDIS_SECRET')]) {
      stage("Set up env") {
        sh 'chmod u+x -R ./jenkins-docker' 
        sh './jenkins-docker/Pre-Build/setup-env.sh'
      }
    }
    stage("Build") {
      sh './jenkins-docker/Jenkins-build/build.sh'
    }
    withCredentials([string(credentialsId: 'redis-secret', variable: 'REDIS_SECRET')]) {
      stage("Test") {
        unitTestStatusCode = sh script:'./jenkins-docker/Test/api-unit-test/api-unit-test.sh', returnStatus: true
        echo "unitTestStatusCode: $unitTestStatusCode"
        integrationTestStatusCode = sh script:'./jenkins-docker/Test/run-test.sh', returnStatus:true
        echo "integrationTestStatusCode $integrationTestStatusCode"
        // sh './jenkins-docker/Test/run-test.sh'

        sh './jenkins-docker/Test/create-logs.sh'
      }
    }
    
  }
  catch (err) {
    currentBuild.result = "FAILURE"

  }
  finally {
    // if (currentBuild.result == 'FAILURE') {
    if (unitTestStatusCode == 1) {
      echo 'UNIT TEST FAILED: Is this intentional?'      
    }
    else if (integrationTestStatusCode == 1) {
      echo 'INTEGRATION TEST FAILED'
    }
    else {
      echo 'TEST SUCEEDED'
      withCredentials([sshUserPrivateKey(credentialsId: 'AWS-EC2', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'username')]) {
        remote.host = "52.8.24.164"
        // remote.host = IP_ADDRESS
        remote.user = username
        remote.identityFile = identity
        stage("Deploy") {
          sshScript remote: remote, script: './jenkins-docker/Deploy/clone-checkout.sh'
          sshPut remote: remote, from: './.env', into: '/home/ubuntu/wordle/', override: true
          sshPut remote: remote, from: './app/services/Redis/redis.conf', into: '/home/ubuntu/wordle/app/services/Redis/', override: true
          sshCommand remote: remote, command: "cd /home/ubuntu/wordle && chmod +x ./bin/server-init.sh && sudo ./bin/server-init.sh"
        }
      }
    }
    // ALWAYS
    sh './jenkins-docker/Post/post.sh'
    archiveArtifacts: 'logs/after-test-docker-logs.txt'
  }
}