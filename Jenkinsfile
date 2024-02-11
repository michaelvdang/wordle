def remote = [:]
remote.name = "EC2 instance"

remote.allowAnyHosts = true
// create credential in Jenkins for EC2 container with id of AWS-EC2 using private key for the container
node {
  withCredentials([file(credentialsId: 'wordle-env-file', variable: 'ENV_FILE_PATH'), file(credentialsId: 'wordle-env-file', variable: 'REDIS_CONF_FILE_PATH'), string(credentialsId: 'redis-secret', variable: 'REDIS_SECRET')]) {
    stage("precheck") {
      sh 'chmod u+x -R ./jenkins-docker'
      sh './jenkins-docker/Pre-Build/pre-build.sh'
    }
    stage("build") {
      sh './jenkins-docker/build.sh'
    }
    stage("test") {
      sh './jenkins-docker/Test/run-test.sh'
    }
    stage("pre-deploy") {
      sh './jenkins-docker/Deploy/pre-deploy.sh'
    }
  }

  withCredentials([sshUserPrivateKey(credentialsId: 'AWS-EC2', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'username')]) {
    remote.host = "52.8.24.164"
    // remote.host = "<IP_ADDRESS>" // for template
    remote.user = username
    remote.identityFile = identity
    stage("Deploy") {
      sshPut remote: remote, from: './jenkins-docker/Deploy/deploy.sh', into: '/home/ubuntu'
      // sshPut remote: remote, from: './jenkins-docker/Deploy/deploy.sh', into: '/wordle/jenkins-docker/Deploy/'
      sshScript remote: remote, script: "deploy.sh"
    }
  }
}