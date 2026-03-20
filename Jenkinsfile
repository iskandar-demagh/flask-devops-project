pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    credentialsId: 'jenkins-ssh-key',
                    url: 'git@github.com:iskandar-demagh/flask-devops-project.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }

        stage('Test') {
            steps {
                sh 'sleep 10' // wait for app to start
                sh '''
                    response=$(curl -s http://localhost:5000/health)
                    echo "Health check response: $response"
                    if echo $response | grep -q "healthy"; then
                        echo "✅ App is healthy!"
                    else
                        echo "❌ App is not healthy!"
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! App is deployed.'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs.'
        }
    }
}
