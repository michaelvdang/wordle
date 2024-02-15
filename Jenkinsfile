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
      }
    }
    
  }
  catch (err) {
    currentBuild.result = "FAILURE"
      // mail body: "project build error is here: ${env.BUILD_URL}" ,
      // from: 'mdang2023@gmail.com',
      // replyTo: 'mdang2023@gmail.com',
      // subject: 'project build failed',
      // to: 'mdang2023@gmail.com'
  }
  finally {
    if (currentBuild.result == 'FAILURE') {
      echo 'BUILD FAILED'
    }
    
    if (currentBuild.result == 'SUCCESS') {
      echo 'BUILD SUCEEDED'
      // withCredentials([sshUserPrivateKey(credentialsId: 'AWS-EC2', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'username')]) {
      //   remote.host = "52.8.24.164"
      //   // remote.host = IP_ADDRESS
      //   remote.user = username
      //   remote.identityFile = identity
      //   stage("Deploy") {
      //     sshScript remote: remote, script: './jenkins-docker/Deploy/clone-checkout.sh'
      //     sshPut remote: remote, from: './.env', into: '/home/ubuntu/wordle/', override: true
      //     sshPut remote: remote, from: './app/services/Redis/redis.conf', into: '/home/ubuntu/wordle/app/services/Redis/', override: true
      //     sshCommand remote: remote, command: "cd /home/ubuntu/wordle && chmod +x ./bin/server-init.sh && sudo ./bin/server-init.sh"
      //   }
      // }
    }
    // ALWAYS
    sh './jenkins-docker/Post/post.sh'
  }
}