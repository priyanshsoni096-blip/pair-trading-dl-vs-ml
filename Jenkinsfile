pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/priyanshsoni096-blip/pair-trading-dl-vs-ml.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality') {
            steps {
                bat '''
                pip install flake8 --quiet
                flake8 src/ --max-line-length=100 --statistics
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                pip install pytest pytest-cov --quiet
                pytest tests/ --cov=src --cov-report=html --cov-report=xml
                '''
            }
            post {
                always {
                    publishHTML(target: [
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: false
                    ])
                }
            }
        }

        stage('Security Scan') {
            steps {
                bat '''
                pip install bandit --quiet
                bandit -r src/ -ll -f json -o bandit-report.json || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t pair-trading-app .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker run -d -p 8888:8888 pair-trading-app'
            }
        }
    }
}