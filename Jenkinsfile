pipeline {
    agent any

    environment {
        IMAGE_NAME = "flight-preictor-api"
        IMAGE_TAG = "latest"
        CONTAINER_NAME = "flight_pred_container"
        DOCKERFILE_DIR = "."  // Update if Dockerfile is in a subdir
    }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        echo "Building Docker image..."
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERFILE_DIR}
                    """
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    sh """
                        if [ \$(docker ps -q -f name=${CONTAINER_NAME}) ]; then
                            echo "Stopping running container..."
                            docker stop ${CONTAINER_NAME}
                        fi
                        if [ \$(docker ps -aq -f name=${CONTAINER_NAME}) ]; then
                            echo "Removing existing container..."
                            docker rm ${CONTAINER_NAME}
                        fi
                    """
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh """
                        echo "Running new container..."
                        docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
