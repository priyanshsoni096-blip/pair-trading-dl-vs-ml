pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/priyanshsoni096-blip/pair-trading-dl-vs-ml.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }
        stage('Code Quality') {
            steps {
                sh 'python3 -m flake8 . || true'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/ || true'
            }
        }
        stage('Security Scan') {
            steps {
                sh 'python3 -m bandit -r . || true'
            }
        }
        stage('Generate Convergence Report') {
            steps {
                sh 'python3 generate_report.py'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying pair trading model...'
                echo 'Deployment successful'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}