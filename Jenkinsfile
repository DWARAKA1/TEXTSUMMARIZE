pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'textsummarize'
        IMAGE_TAG = 'latest'
        DOCKER_IMAGE = "${DOCKER_REGISTRY}:${IMAGE_TAG}"
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    echo 'Setting up Python environment...'
                    sh 'python --version'
                    sh 'pip install --upgrade pip'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Installing dependencies...'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running unit tests...'
                    sh 'pytest tests/ -v --tb=short'
                }
            }
        }

        stage('Validate Structure') {
            steps {
                script {
                    echo 'Validating project structure...'
                    sh 'test -d tests'
                    sh 'test -f main.py'
                    sh 'test -f streamlit.py'
                    sh 'echo "Project structure valid"'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }

        stage('Test Docker Image') {
            steps {
                script {
                    echo 'Testing Docker image...'
                    sh 'docker run --rm ${DOCKER_IMAGE} python -c "import nltk; print(\"Dependencies loaded successfully\")"'
                }
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
        always {
            echo 'Cleaning up...'
        }
    }
}
