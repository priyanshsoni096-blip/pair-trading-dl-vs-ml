pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "No tests yet"'
            }
        }
    }
}