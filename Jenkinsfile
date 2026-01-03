pipeline {

    agent any

    environment {
        PYTHON_VERSION="3.12"
    }
    
    triggers {
        githubPush()
    }

    stages {

        stage("Environment") {
            steps {
               sh """
               env | sort
               """
            }
        }

        stage("Checkout") {
            steps {
                checkout scm
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}