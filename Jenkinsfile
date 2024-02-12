def remote = [:]
remote.name = "EC2 instance"

remote.allowAnyHosts = true
// create credential in Jenkins for EC2 container with id of AWS-EC2 using private key for the container
node {
  currentBuild.result = "SUCCESS"
  try {
    stage("Checkout") {
      checkout scm
    }
    withCredentials([file(credentialsId: 'wordle-env-file', variable: 'ENV_FILE_PATH'), file(credentialsId: 'wordle-env-file', variable: 'REDIS_CONF_FILE_PATH'), string(credentialsId: 'redis-secret', variable: 'REDIS_SECRET')]) {
      stage("precheck") {
        sh 'chmod u+x -R ./jenkins-docker'
        sh './jenkins-docker/Pre-Build/pre-build.sh'
      }
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

    // withCredentials([sshUserPrivateKey(credentialsId: 'AWS-EC2', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'username')]) {
    //   remote.host = "52.8.24.164"
    //   // remote.host = "<IP_ADDRESS>" // for template
    //   remote.user = username
    //   remote.identityFile = identity
    //   stage("Deploy") {
    //     // sshPut remote: remote, from: './jenkins-docker/Deploy/deploy.sh', into: '/home/ubuntu/'
    //     // sshPut remote: remote, from: './jenkins-docker/Deploy/deploy.sh', into: '/wordle/jenkins-docker/Deploy/'
    //     sshScript remote: remote, script: "./jenkins-docker/Deploy/deploy.sh"
    //   }
    // }
  catch (err) {
    currentBuild.result = "FAILURE"
      // mail body: "project build error is here: ${env.BUILD_URL}" ,
      // from: 'mdang2023@gmail.com',
      // replyTo: 'mdang2023@gmail.com',
      // subject: 'project build failed',
      // to: 'mdang2023@gmail.com'
  }
  finally {
    sh './jenkins-docker/Post/post.sh'
  }
}