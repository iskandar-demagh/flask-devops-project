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

        stage('Push to Docker Hub') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'dockerhub-credentials',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
        )]) {
            sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
            sh 'docker tag flask-devops-project-web:latest $DOCKER_USER/flask-devops-project:latest'
            sh 'docker push $DOCKER_USER/flask-devops-project:latest'
        }
    }
} 
        stage('Deploy') {
    steps {
        // Stop containers from Jenkins workspace
        sh 'docker compose down || true'

        // Stop ANY container using port 5000
        sh '''
            container=$(docker ps -q --filter "publish=5000")
            if [ -n "$container" ]; then
                echo "Stopping container using port 5000: $container"
                docker stop $container
                docker rm $container
            fi
        '''

        // Start fresh
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
