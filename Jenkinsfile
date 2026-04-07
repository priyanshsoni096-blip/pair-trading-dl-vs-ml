pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "pair-trading-ml"
        IMAGE_TAG = "latest"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/priyanshsoni096-blip/pair-trading-dl-vs-ml'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running pytest unit tests...'
                sh 'python -m pytest tests/ -v --tb=short'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        
        stage('Deploy Container') {
            steps {
                echo 'Deploying container...'
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }
    }
    
    post {
        success {
            echo ' Pipeline passed — Jupyter live at localhost:8888'
        }
        failure {
            echo ' Pipeline failed — check logs above'
        }
    }
}