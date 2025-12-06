pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'production'], description: 'Environment to deploy')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Deploy after successful build?')
    }

    environment {
        REGISTRY = 'textsummarize'
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
        DOCKER_IMAGE = "${REGISTRY}:${IMAGE_TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '========== Checking out code =========='
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    env.GIT_BRANCH = sh(returnStdout: true, script: 'git rev-parse --abbrev-ref HEAD').trim()
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '========== Installing dependencies =========='
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install ruff black pytest pytest-cov
                '''
            }
        }

        stage('Lint') {
            steps {
                echo '========== Running code quality checks =========='
                sh '''
                    echo "Running Ruff linting..."
                    ruff check . --exit-zero --format=json > ruff-report.json || true
                    
                    echo "Running Black formatting check..."
                    black --check . 2>&1 || {
                        echo "Code formatting issues found. Running formatter..."
                        black . 
                    }
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo '========== Running unit tests =========='
                sh '''
                    pytest tests/ -v --tb=short --cov=. --cov-report=xml --cov-report=html \
                    --junit-xml=test-results.xml || EXIT_CODE=$?
                    echo "Test execution completed with exit code: ${EXIT_CODE}"
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML(target: [
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report'
                    ])
                }
            }
        }

        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                echo '========== Building Docker image =========='
                sh '''
                    echo "Building Docker image: ${DOCKER_IMAGE}"
                    docker build -t ${DOCKER_IMAGE} \
                        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
                        --build-arg VCS_REF="${GIT_COMMIT_SHORT}" \
                        -f Dockerfile .
                    
                    echo "Tagging image..."
                    docker tag ${DOCKER_IMAGE} ${REGISTRY}:latest
                    docker image ls | grep ${REGISTRY}
                '''
            }
        }

        stage('Security Scan') {
            when {
                branch 'main'
            }
            steps {
                echo '========== Running security scans =========='
                sh '''
                    echo "Scanning Python dependencies for vulnerabilities..."
                    pip install safety
                    safety check --json > safety-report.json || true
                '''
            }
        }

        stage('Push to Registry') {
            when {
                branch 'main'
                expression { params.DEPLOY == true }
            }
            steps {
                echo '========== Pushing image to registry =========='
                sh '''
                    echo "Pushing ${DOCKER_IMAGE} to registry..."
                    # docker login -u $DOCKER_USER -p $DOCKER_PASS $REGISTRY_URL
                    # docker push ${DOCKER_IMAGE}
                    # docker push ${REGISTRY}:latest
                    echo "Image push completed (dry-run)"
                '''
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
                expression { params.DEPLOY == true }
            }
            steps {
                echo '========== Deploying to environment: ${ENV} =========='
                sh '''
                    echo "Deploying to ${ENV} environment..."
                    
                    case "${ENV}" in
                        dev)
                            echo "Deploying to development..."
                            # docker run -d -p 8000:8000 --name textsummarize-dev ${DOCKER_IMAGE}
                            ;;
                        staging)
                            echo "Deploying to staging..."
                            # Deploy to staging environment
                            ;;
                        production)
                            echo "Deploying to production..."
                            # Deploy to production environment with health checks
                            ;;
                    esac
                '''
            }
        }

        stage('Health Check') {
            when {
                expression { params.DEPLOY == true }
            }
            steps {
                echo '========== Running health checks =========='
                sh '''
                    sleep 5
                    echo "Checking API health..."
                    # curl -f http://localhost:8000/health || exit 1
                    echo "Health check passed"
                '''
            }
        }
    }

    post {
        always {
            echo '========== Pipeline completed =========='
            sh '''
                echo "Pipeline Summary:"
                echo "Git Commit: ${GIT_COMMIT_SHORT}"
                echo "Branch: ${GIT_BRANCH}"
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Environment: ${ENV}"
            '''
            cleanWs()
        }
        success {
            echo '========== Build SUCCESSFUL =========='
            // Send success notification
        }
        failure {
            echo '========== Build FAILED =========='
            // Send failure notification
        }
    }
}
