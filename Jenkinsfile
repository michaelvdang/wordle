pipeline {

  // agent { label "linux" }
  agent any

  stages {

    stage("build") {

      environment {
        SECRET_FILE_CONTENT = credentials('wordle-env-file')
      }

      steps {
        sh 'printenv'
        echo 'building the application..'
        sh '''
          pwd
          cd 
          pwd
          ls 
          echo hi
          echo ${SECRET_FILE_CONTENT}

        '''
      }
      
    }

    stage("test") {

      steps {
        echo 'testing the application..'

      }
      
    }
    
  }

}