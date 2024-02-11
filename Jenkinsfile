def remote = [:]
remote.name = "node-1"

remote.allowAnyHosts = true
// create credential in Jenkins for EC2 container with id of AWS-EC2 using private key for the container
node {
  withCredentials([file(credentialsId: 'wordle-env-file', variable: 'ENV_FILE_PATH'), file(credentialsId: 'wordle-env-file', variable: 'REDIS_CONF_FILE_PATH'), string(credentialsId: 'redis-secret', variable: 'REDIS_SECRET')]) {
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

  withCredentials([sshUserPrivateKey(credentialsId: 'AWS-EC2', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'username')]) {
    remote.host = "52.8.24.164"
    // remote.host = "<IP_ADDRESS>" // for template
    remote.user = username
    remote.identityFile = identity
    stage("SSH Steps Rocks!") {
      sshPut remote: remote, from: 'deploy.sh', into: '/wordle/jenkins-docker/Deploy/'
      sshScript remote: remote, script: "deploy.sh"
    }
  }
}