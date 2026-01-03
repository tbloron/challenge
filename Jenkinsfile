pipeline {
    agent any
    environment {
        PYTHON_VERSION="3.12"
    }

    stages {
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